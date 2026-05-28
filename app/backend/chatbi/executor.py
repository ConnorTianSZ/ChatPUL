from collections import defaultdict
from datetime import date
from typing import Any

from app.backend.chatbi.calculations import (
    empty_oc_buckets,
    empty_pr_buckets,
    parse_date,
    po_confirmation_lead_time_bucket,
    pr_lead_time_bucket,
)
from app.backend.chatbi.field_dictionary import source_trace_entry
from app.backend.chatbi.models import (
    AutoPoRatioToolCall,
    CommonFilters,
    CountSort,
    LeadTimeToolCall,
    ManufacturerDimensionToolCall,
    RatioSort,
    SupplierDimensionToolCall,
    TimeRange,
    ToolCall,
    filters_or_default,
    time_range_or_default,
)
from app.backend.chatbi.repository import DummyPoItemRepository


DATE_FIELD_HEADERS = {
    "doc_date": "Doc. Date",
    "pr_date": "PR Date",
    "order_confirmation_date": "order confirmatioin date",
    "goods_receipt_posting_date": "GR-D.o.Post",
    "statistical_delivery_date": "S.Del.Dat",
}

GROUP_FIELD_NAMES = {
    "supplier": "supplier_code",
    "buyer": "buyer_key",
    "manufacturer": "manufacturer_name",
    "wbs_status": "wbs_status",
    "plant": "plant",
    "mrp_type": "mrp_type",
    "month": "reporting_month",
    "none": "po_item_count",
}


def execute_tool_call(call: ToolCall, repository: DummyPoItemRepository) -> dict[str, Any]:
    rows = repository.list_rows()
    filters = filters_or_default(call.arguments.filters)
    time_range = time_range_or_default(call.arguments.time_range)
    filtered_rows = apply_filters(rows, filters, time_range)

    if isinstance(call, SupplierDimensionToolCall):
        return execute_dimension_tool(call.tool, call.arguments, filtered_rows, filters, time_range, repository)
    if isinstance(call, ManufacturerDimensionToolCall):
        return execute_dimension_tool(call.tool, call.arguments, filtered_rows, filters, time_range, repository)
    if isinstance(call, LeadTimeToolCall):
        return execute_lead_time_tool(call, filtered_rows, filters, time_range, repository)
    if isinstance(call, AutoPoRatioToolCall):
        return execute_auto_po_ratio_tool(call, filtered_rows, filters, time_range, repository)

    raise ValueError("Unsupported tool call")


def apply_filters(rows: list[dict[str, str]], filters: CommonFilters, time_range: TimeRange) -> list[dict[str, str]]:
    return [row for row in rows if row_matches_filters(row, filters, time_range)]


def row_matches_filters(row: dict[str, str], filters: CommonFilters, time_range: TimeRange) -> bool:
    if filters.buyer_keys is not None and row["PGr"] not in filters.buyer_keys:
        return False
    if filters.supplier_codes is not None and row["Vendor"] not in filters.supplier_codes:
        return False
    if filters.supplier_names is not None and row["Name 1"] not in filters.supplier_names:
        return False
    if filters.plants is not None and row["Plant"] not in filters.plants:
        return False
    if filters.mrp_types is not None and row["MRP Type"] not in filters.mrp_types:
        return False

    manufacturer = blank_bucket(row["Manufactur"])
    if filters.manufacturer_names is not None:
        requested = {"<BLANK>" if value == "" else value for value in filters.manufacturer_names}
        if manufacturer not in requested:
            return False
    elif not filters.include_blank_manufacturer and manufacturer == "<BLANK>":
        return False

    if filters.wbs_scope == "with_wbs" and row["WBS element"] == "":
        return False
    if filters.wbs_scope == "blank_wbs" and row["WBS element"] != "":
        return False

    row_date = parse_date(row[DATE_FIELD_HEADERS[time_range.date_field]])
    if (time_range.from_ is not None or time_range.to is not None) and row_date is None:
        return False
    if time_range.from_ is not None and row_date is not None and row_date < parse_required_date(time_range.from_):
        return False
    if time_range.to is not None and row_date is not None and row_date > parse_required_date(time_range.to):
        return False

    return True


def parse_required_date(value: str) -> date:
    parsed = parse_date(value)
    if parsed is None:
        raise ValueError("Expected non-empty date")
    return parsed


def blank_bucket(value: str) -> str:
    if value == "":
        return "<BLANK>"
    return value


def group_key(row: dict[str, str], group_by: str) -> str:
    if group_by == "supplier":
        return row["Vendor"]
    if group_by == "buyer":
        return row["PGr"]
    if group_by == "manufacturer":
        return blank_bucket(row["Manufactur"])
    if group_by == "wbs_status":
        return "blank_wbs" if row["WBS element"] == "" else "with_wbs"
    if group_by == "plant":
        return row["Plant"]
    if group_by == "mrp_type":
        return row["MRP Type"]
    if group_by == "month":
        return row["Doc. Date"][:7]
    raise ValueError(f"Unsupported group_by: {group_by}")


def execute_dimension_tool(
    tool: str,
    arguments: Any,
    rows: list[dict[str, str]],
    filters: CommonFilters,
    time_range: TimeRange,
    repository: DummyPoItemRepository,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[group_key(row, arguments.group_by)].append(row)

    result_rows = []
    for key, group_rows in grouped.items():
        result_row: dict[str, Any] = {"group_key": key, "po_item_count": len(group_rows)}
        if arguments.group_by == "supplier":
            result_row["supplier_code"] = key
            result_row["supplier_name"] = group_rows[0]["Name 1"]
        if arguments.group_by == "manufacturer":
            result_row["is_blank_manufacturer"] = key == "<BLANK>"
        result_rows.append(result_row)

    result_rows = sort_count_rows(result_rows, arguments.sort)
    if arguments.limit is not None:
        result_rows = result_rows[: arguments.limit]

    field_names = fields_for_dimension_tool(arguments.group_by)
    return {
        "tool": tool,
        "understood_request": execution_summary(tool, arguments.group_by),
        "group_by": arguments.group_by,
        "filters_applied": filters_dump(filters),
        "rows": result_rows,
        "total": len(rows),
        "source_trace": build_source_trace(tool, arguments.group_by, filters, time_range, field_names, repository),
    }


def sort_count_rows(rows: list[dict[str, Any]], sort: CountSort | None) -> list[dict[str, Any]]:
    sort_by = sort.by if sort is not None and sort.by is not None else "po_item_count"
    reverse = sort is None or sort.direction == "desc"
    return sorted(rows, key=lambda row: count_sort_key(row, sort_by), reverse=reverse)


def count_sort_key(row: dict[str, Any], sort_by: str) -> tuple[Any, str]:
    if sort_by == "group_key":
        return (row["group_key"], row["group_key"])
    return (row["po_item_count"], row["group_key"])


def execute_auto_po_ratio_tool(
    call: AutoPoRatioToolCall,
    rows: list[dict[str, str]],
    filters: CommonFilters,
    time_range: TimeRange,
    repository: DummyPoItemRepository,
) -> dict[str, Any]:
    field_names = fields_for_auto_po_ratio_tool(call.arguments.group_by)
    result: dict[str, Any] = {
        "tool": call.tool,
        "understood_request": execution_summary(call.tool, call.arguments.group_by),
        "group_by": call.arguments.group_by,
        "numerator_rule": "PO created by = UC4CPIC",
        "filters_applied": filters_dump(filters),
        "source_trace": build_source_trace(
            call.tool,
            call.arguments.group_by,
            filters,
            time_range,
            field_names,
            repository,
        ),
    }

    if call.arguments.group_by == "none":
        result["overall"] = ratio_entry(rows)
        return result

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[group_key(row, call.arguments.group_by)].append(row)

    groups = []
    for key, group_rows in grouped.items():
        group = {"group_key": key, **ratio_entry(group_rows)}
        if call.arguments.group_by == "manufacturer":
            group["is_blank_manufacturer"] = key == "<BLANK>"
        groups.append(group)

    groups = sort_ratio_rows(groups, call.arguments.sort)
    if call.arguments.limit is not None:
        groups = groups[: call.arguments.limit]
    result["groups"] = groups
    return result


def ratio_entry(rows: list[dict[str, str]]) -> dict[str, Any]:
    total = len(rows)
    uc4_count = sum(1 for row in rows if row["PO created by"] == "UC4CPIC")
    ratio = 0.0 if total == 0 else round(uc4_count / total, 6)
    return {"uc4_count": uc4_count, "total": total, "ratio": ratio}


def sort_ratio_rows(rows: list[dict[str, Any]], sort: RatioSort | None) -> list[dict[str, Any]]:
    sort_by = sort.by if sort is not None and sort.by is not None else "ratio"
    reverse = sort is None or sort.direction == "desc"
    return sorted(rows, key=lambda row: ratio_sort_key(row, sort_by), reverse=reverse)


def ratio_sort_key(row: dict[str, Any], sort_by: str) -> tuple[Any, str]:
    if sort_by == "group_key":
        return (row["group_key"], row["group_key"])
    return (row[sort_by], row["group_key"])


def execute_lead_time_tool(
    call: LeadTimeToolCall,
    rows: list[dict[str, str]],
    filters: CommonFilters,
    time_range: TimeRange,
    repository: DummyPoItemRepository,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "tool": call.tool,
        "understood_request": execution_summary(call.tool, call.arguments.group_by),
        "lead_time_type": call.arguments.lead_time_type,
        "group_by": call.arguments.group_by,
        "filters_applied": filters_dump(filters),
        "calculation_note": (
            "PR lead time uses NETWORKDAYS(PR Date, Doc. Date) - 1. "
            "PO confirmation lead time uses NETWORKDAYS(Doc. Date, order confirmatioin date) - 1. "
            "Working days are Monday through Friday with no holiday calendar."
        ),
        "source_trace": build_source_trace(
            call.tool,
            call.arguments.group_by,
            filters,
            time_range,
            fields_for_lead_time_tool(call.arguments.group_by),
            repository,
        ),
    }

    if call.arguments.lead_time_type in ("pr", "both"):
        result["pr_buckets"] = pr_bucket_counts(rows)
    if call.arguments.lead_time_type in ("po_confirmation", "both"):
        result["po_confirmation_buckets"] = po_confirmation_bucket_counts(rows)

    if call.arguments.group_by != "none":
        grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            grouped[group_key(row, call.arguments.group_by)].append(row)

        groups = []
        for key, group_rows in grouped.items():
            group: dict[str, Any] = {"group_key": key}
            if call.arguments.group_by == "manufacturer":
                group["is_blank_manufacturer"] = key == "<BLANK>"
            if call.arguments.lead_time_type in ("pr", "both"):
                group["pr_buckets"] = pr_bucket_counts(group_rows)
            if call.arguments.lead_time_type in ("po_confirmation", "both"):
                group["po_confirmation_buckets"] = po_confirmation_bucket_counts(group_rows)
            groups.append(group)
        result["groups"] = sorted(groups, key=lambda row: row["group_key"])

    return result


def pr_bucket_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts = empty_pr_buckets()
    for row in rows:
        counts[pr_lead_time_bucket(row)] += 1
    return counts


def po_confirmation_bucket_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    counts = empty_oc_buckets()
    for row in rows:
        counts[po_confirmation_lead_time_bucket(row)] += 1
    return counts


def execution_summary(tool: str, group_by: str) -> str:
    return f"Executed {tool} grouped by {group_by} against dummy PO-item data."


def filters_dump(filters: CommonFilters) -> dict[str, Any]:
    return filters.model_dump(exclude_none=True)


def time_range_dump(time_range: TimeRange) -> dict[str, Any]:
    return time_range.model_dump(by_alias=True, exclude_none=True)


def fields_for_dimension_tool(group_by: str) -> list[str]:
    fields = ["po_item_count", GROUP_FIELD_NAMES[group_by]]
    if group_by == "supplier":
        fields.append("supplier_name")
    return dedupe_fields(fields + ["doc_date"])


def fields_for_auto_po_ratio_tool(group_by: str) -> list[str]:
    return dedupe_fields(["po_created_by", "uc4_count", "auto_po_ratio", "po_item_count", GROUP_FIELD_NAMES[group_by]])


def fields_for_lead_time_tool(group_by: str) -> list[str]:
    return dedupe_fields(
        [
            "pr_date",
            "doc_date",
            "order_confirmation_date",
            "goods_receipt_posting_date",
            "pr_lead_time_bucket",
            "po_confirmation_lead_time_bucket",
            GROUP_FIELD_NAMES[group_by],
        ]
    )


def dedupe_fields(field_names: list[str]) -> list[str]:
    seen = set()
    result = []
    for field_name in field_names:
        if field_name not in seen:
            result.append(field_name)
            seen.add(field_name)
    return result


def build_source_trace(
    tool: str,
    group_by: str,
    filters: CommonFilters,
    time_range: TimeRange,
    field_names: list[str],
    repository: DummyPoItemRepository,
) -> dict[str, Any]:
    source_field_names = dedupe_fields(field_names + active_filter_field_names(filters) + [time_range.date_field])
    return {
        "dataset": repository.metadata,
        "tool": tool,
        "group_by": group_by,
        "filters_applied": filters_dump(filters),
        "time_range_applied": time_range_dump(time_range),
        "source_columns": [source_trace_entry(field_name) for field_name in source_field_names],
    }


def active_filter_field_names(filters: CommonFilters) -> list[str]:
    field_names = []
    if filters.buyer_keys is not None:
        field_names.append("buyer_key")
    if filters.supplier_codes is not None:
        field_names.append("supplier_code")
    if filters.supplier_names is not None:
        field_names.append("supplier_name")
    if filters.manufacturer_names is not None or not filters.include_blank_manufacturer:
        field_names.append("manufacturer_name")
    if filters.wbs_scope != "all":
        field_names.append("wbs_status")
    if filters.plants is not None:
        field_names.append("plant")
    if filters.mrp_types is not None:
        field_names.append("mrp_type")
    return field_names
