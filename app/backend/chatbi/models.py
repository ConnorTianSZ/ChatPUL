from datetime import date as date_type
from typing import Annotated, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_validator, model_validator


DateField = Literal[
    "doc_date",
    "pr_date",
    "order_confirmation_date",
    "goods_receipt_posting_date",
    "statistical_delivery_date",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class TimeRange(StrictModel):
    date_field: DateField = "doc_date"
    from_: str | None = Field(default=None, alias="from", pattern=r"^\d{4}-\d{2}-\d{2}$")
    to: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$")

    @field_validator("from_", "to")
    @classmethod
    def validate_calendar_date(cls, v: str | None) -> str | None:
        if v is None:
            return v
        try:
            y, m, d = map(int, v.split("-"))
            date_type(y, m, d)
        except (ValueError, TypeError):
            raise ValueError(f"invalid calendar date: {v}")
        return v


class CommonFilters(StrictModel):
    buyer_keys: list[str] | None = None
    supplier_codes: list[str] | None = None
    supplier_names: list[str] | None = None
    manufacturer_names: list[str] | None = None
    include_blank_manufacturer: bool = True
    wbs_scope: Literal["all", "with_wbs", "blank_wbs"] = "all"
    plants: list[str] | None = None
    mrp_types: list[str] | None = None


class ChatBIAskRequest(StrictModel):
    question: str = Field(min_length=1)


class CountSort(StrictModel):
    by: Literal["po_item_count", "group_key"] | None = None
    direction: Literal["asc", "desc"] = "desc"


class RatioSort(StrictModel):
    by: Literal["ratio", "uc4_count", "total", "group_key"] | None = None
    direction: Literal["asc", "desc"] = "desc"


class SupplierDimensionArguments(StrictModel):
    group_by: Literal["supplier", "buyer", "manufacturer", "wbs_status", "plant", "mrp_type", "month"]
    time_range: TimeRange | None = None
    filters: CommonFilters | None = None
    sort: CountSort | None = None
    limit: int | None = Field(default=None, ge=1, le=100)


class ManufacturerDimensionArguments(StrictModel):
    group_by: Literal["manufacturer", "buyer", "supplier", "wbs_status", "plant", "mrp_type", "month"]
    time_range: TimeRange | None = None
    filters: CommonFilters | None = None
    sort: CountSort | None = None
    limit: int | None = Field(default=None, ge=1, le=100)


class LeadTimeArguments(StrictModel):
    lead_time_type: Literal["pr", "po_confirmation", "both"]
    group_by: Literal["none", "buyer", "manufacturer", "supplier", "month"]
    time_range: TimeRange | None = None
    filters: CommonFilters | None = None

    @model_validator(mode="after")
    def reject_statistical_delivery_date(self):
        if self.time_range is not None and self.time_range.date_field == "statistical_delivery_date":
            raise ValueError(
                "date_field 'statistical_delivery_date' is not supported for lead_time_summary"
            )
        return self


class AutoPoRatioArguments(StrictModel):
    group_by: Literal["none", "buyer", "manufacturer", "supplier", "month"]
    numerator_rule: Literal["po_created_by_equals_uc4cpic"] | None = "po_created_by_equals_uc4cpic"
    time_range: TimeRange | None = None
    filters: CommonFilters | None = None
    sort: RatioSort | None = None
    limit: int | None = Field(default=None, ge=1, le=100)


class SupplierDimensionToolCall(StrictModel):
    tool: Literal["supplier_dimension_summary"]
    arguments: SupplierDimensionArguments


class ManufacturerDimensionToolCall(StrictModel):
    tool: Literal["manufacturer_dimension_summary"]
    arguments: ManufacturerDimensionArguments


class LeadTimeToolCall(StrictModel):
    tool: Literal["lead_time_summary"]
    arguments: LeadTimeArguments


class AutoPoRatioToolCall(StrictModel):
    tool: Literal["auto_po_ratio_summary"]
    arguments: AutoPoRatioArguments


ToolCall = Annotated[
    Union[
        SupplierDimensionToolCall,
        ManufacturerDimensionToolCall,
        LeadTimeToolCall,
        AutoPoRatioToolCall,
    ],
    Field(discriminator="tool"),
]

TOOL_CALL_ADAPTER = TypeAdapter(ToolCall)


def parse_tool_call(payload: object) -> ToolCall:
    return TOOL_CALL_ADAPTER.validate_python(payload)


def filters_or_default(filters: CommonFilters | None) -> CommonFilters:
    if filters is None:
        return CommonFilters()
    return filters


def time_range_or_default(time_range: TimeRange | None) -> TimeRange:
    if time_range is None:
        return TimeRange()
    return time_range
