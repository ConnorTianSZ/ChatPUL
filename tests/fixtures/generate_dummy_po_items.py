import csv
import json
import random
from datetime import date, timedelta


SEED = 20260528
ROW_COUNT = 300
CSV_PATH = "data/dummy/dummy_po_items.csv"
JSON_PATH = "data/dummy/dummy_po_items_expected.json"
README_PATH = "data/dummy/dummy_po_items_README.md"

CSV_COLUMNS = [
    "WBS element",
    "PGr",
    "Vendor",
    "Name 1",
    "Doc. No.",
    "Item",
    "Material",
    "Short Text",
    "MPN",
    "Manufactur",
    "Quantity",
    "Net Price",
    "Net Value Domestic Currency",
    "Crcy",
    "Doc. Date",
    "PR Date",
    "order confirmatioin date",
    "GR-D.o.Post",
    "S.Del.Dat",
    "PO created by",
    "Plant",
    "MRP Type",
]

BUYERS = ["MFA", "MFB", "MFC", "MFD"]
MANUFACTURERS = ["DummyMfr-X", "DummyMfr-Y", "DummyMfr-Z"]
CREATORS = ["UC4CPIC", "ZUSER1", "ZUSER2"]
PLANTS = ["P001", "P002"]
MRP_TYPES = ["ND", "PD"]
SUPPLIER_NAMES = [
    "Dummy Supplier A",
    "Dummy Supplier B",
    "Dummy Supplier C",
    "Dummy Supplier D",
    "Dummy Supplier E",
    "Dummy Supplier F",
    "Dummy Supplier G",
    "Dummy Supplier H",
    "Dummy Supplier I",
    "Dummy Supplier J",
]
SHORT_TEXTS = [
    "Dummy bracket assembly",
    "Dummy cable set",
    "Dummy machined plate",
    "Dummy sensor kit",
    "Dummy service package",
]

PR_BUCKETS = ["0<=X<=3", "3<X<=7", ">7days", "not statistic"]
OC_BUCKETS = ["<=3", "3<X<=7", ">7", "no order confirmation", "Delivered without OC"]

LEAD_TEMPLATES = [
    {
        "pr_date": "2026-01-05",
        "doc_date": "2026-01-07",
        "oc_date": "2026-01-09",
        "gr_date": "",
        "s_del_date": "2026-01-16",
    },
    {
        "pr_date": "2026-01-05",
        "doc_date": "2026-01-12",
        "oc_date": "2026-01-19",
        "gr_date": "",
        "s_del_date": "2026-01-23",
    },
    {
        "pr_date": "2026-01-05",
        "doc_date": "2026-01-20",
        "oc_date": "2026-02-03",
        "gr_date": "",
        "s_del_date": "2026-02-10",
    },
    {
        "pr_date": "",
        "doc_date": "2026-02-02",
        "oc_date": "",
        "gr_date": "",
        "s_del_date": "2026-02-16",
    },
    {
        "pr_date": "",
        "doc_date": "2026-02-03",
        "oc_date": "",
        "gr_date": "2026-02-10",
        "s_del_date": "2026-02-17",
    },
    {
        "pr_date": "2026-03-02",
        "doc_date": "2026-03-05",
        "oc_date": "",
        "gr_date": "2026-03-12",
        "s_del_date": "2026-03-19",
    },
    {
        "pr_date": "2026-03-02",
        "doc_date": "2026-03-10",
        "oc_date": "",
        "gr_date": "2026-03-17",
        "s_del_date": "2026-03-24",
    },
    {
        "pr_date": "2026-04-01",
        "doc_date": "2026-04-15",
        "oc_date": "2026-04-17",
        "gr_date": "",
        "s_del_date": "2026-04-24",
    },
]


def make_doc_item(index):
    doc_no = str(90000001 + index // 3).zfill(8)
    item = str(((index % 3) + 1) * 10).zfill(5)
    return doc_no, item


def make_project_wbs(index):
    station = 800 + (index % 5) * 10
    suffix = 1 if index % 2 == 0 else 5
    return "M.6601336." + str(station) + ".0." + str(suffix)


def make_material(index, manufacturer):
    if manufacturer == "" or index % 7 == 0:
        return "DUMMY-MAT-" + str((index % 40) + 1).zfill(3)
    return "9999." + str((index % 80) + 1).zfill(3) + "." + str((index % 20) + 1).zfill(3)


def make_row(index, pgr, manufacturer, wbs, creator, template, rng):
    doc_no, item = make_doc_item(index)
    supplier_index = index % len(SUPPLIER_NAMES)
    quantity = rng.randint(1, 20)
    net_price = rng.randint(20, 450)
    net_value = quantity * net_price
    material = make_material(index, manufacturer)
    return {
        "WBS element": wbs,
        "PGr": pgr,
        "Vendor": str(80000001 + supplier_index),
        "Name 1": SUPPLIER_NAMES[supplier_index],
        "Doc. No.": doc_no,
        "Item": item,
        "Material": material,
        "Short Text": SHORT_TEXTS[index % len(SHORT_TEXTS)],
        "MPN": "DUMMY-MPN-" + str(index + 1).zfill(4),
        "Manufactur": manufacturer,
        "Quantity": str(quantity),
        "Net Price": str(net_price),
        "Net Value Domestic Currency": str(net_value),
        "Crcy": "CNY",
        "Doc. Date": template["doc_date"],
        "PR Date": template["pr_date"],
        "order confirmatioin date": template["oc_date"],
        "GR-D.o.Post": template["gr_date"],
        "S.Del.Dat": template["s_del_date"],
        "PO created by": creator,
        "Plant": PLANTS[index % len(PLANTS)],
        "MRP Type": MRP_TYPES[index % len(MRP_TYPES)],
    }


def generate_rows():
    rng = random.Random(SEED)
    rows = []

    for i in range(12):
        rows.append(
            make_row(
                len(rows),
                BUYERS[i % len(BUYERS)],
                "",
                "" if i < 6 else make_project_wbs(i),
                ["UC4CPIC", "ZUSER1", "UC4CPIC", "ZUSER2"][i % 4],
                LEAD_TEMPLATES[i % len(LEAD_TEMPLATES)],
                rng,
            )
        )

    for i in range(24):
        rows.append(
            make_row(
                len(rows),
                BUYERS[i % len(BUYERS)],
                MANUFACTURERS[i % len(MANUFACTURERS)],
                "",
                CREATORS[i % len(CREATORS)],
                LEAD_TEMPLATES[(i + 2) % len(LEAD_TEMPLATES)],
                rng,
            )
        )

    for i in range(36):
        rows.append(
            make_row(
                len(rows),
                BUYERS[i % len(BUYERS)],
                MANUFACTURERS[i % len(MANUFACTURERS)],
                make_project_wbs(i),
                CREATORS[(i + 1) % len(CREATORS)],
                LEAD_TEMPLATES[(i + 4) % len(LEAD_TEMPLATES)],
                rng,
            )
        )

    while len(rows) < ROW_COUNT:
        index = len(rows)
        manufacturer_choices = MANUFACTURERS + MANUFACTURERS + [""]
        manufacturer = rng.choice(manufacturer_choices)
        wbs = "" if rng.random() < 0.30 else make_project_wbs(index)
        creator = "UC4CPIC" if rng.random() < 0.35 else rng.choice(["ZUSER1", "ZUSER2"])
        rows.append(
            make_row(
                index,
                rng.choice(BUYERS),
                manufacturer,
                wbs,
                creator,
                rng.choice(LEAD_TEMPLATES),
                rng,
            )
        )

    return rows


def expected_parse_date(value):
    parts = value.split("-")
    return date(int(parts[0]), int(parts[1]), int(parts[2]))


def expected_networkdays(start_value, end_value):
    start = expected_parse_date(start_value)
    end = expected_parse_date(end_value)
    current = start
    total = 0
    while current <= end:
        if current.weekday() < 5:
            total += 1
        current += timedelta(days=1)
    return total


def expected_pr_bucket(row):
    if row["PR Date"] == "":
        return "not statistic"
    lead_time = expected_networkdays(row["PR Date"], row["Doc. Date"]) - 1
    if 0 <= lead_time <= 3:
        return "0<=X<=3"
    if 3 < lead_time <= 7:
        return "3<X<=7"
    if lead_time > 7:
        return ">7days"
    return "not statistic"


def expected_oc_bucket(row):
    if row["order confirmatioin date"] == "":
        if row["GR-D.o.Post"] != "":
            return "Delivered without OC"
        return "no order confirmation"
    lead_time = expected_networkdays(row["Doc. Date"], row["order confirmatioin date"]) - 1
    if lead_time <= 3:
        return "<=3"
    if 3 < lead_time <= 7:
        return "3<X<=7"
    return ">7"


def ratio_entry(uc4_count, total):
    ratio = 0.0
    if total:
        ratio = round(uc4_count / total, 6)
    return {"uc4_count": uc4_count, "total": total, "ratio": ratio}


def blank_bucket(value):
    if value == "":
        return "<BLANK>"
    return value


def empty_pr_bucket_counts():
    return {bucket: 0 for bucket in PR_BUCKETS}


def empty_oc_bucket_counts():
    return {bucket: 0 for bucket in OC_BUCKETS}


def compute_expected_stats(rows):
    manufacturer_distribution = {"DummyMfr-X": 0, "DummyMfr-Y": 0, "DummyMfr-Z": 0, "<BLANK>": 0}
    wbs_distribution = {"with_wbs": 0, "blank_wbs": 0}

    overall_uc4 = 0
    by_buyer_counts = {buyer: {"uc4_count": 0, "total": 0} for buyer in BUYERS}
    by_manufacturer_counts = {
        "DummyMfr-X": {"uc4_count": 0, "total": 0},
        "DummyMfr-Y": {"uc4_count": 0, "total": 0},
        "DummyMfr-Z": {"uc4_count": 0, "total": 0},
        "<BLANK>": {"uc4_count": 0, "total": 0},
    }
    pr_buckets = empty_pr_bucket_counts()
    oc_buckets = empty_oc_bucket_counts()
    pr_by_buyer = {buyer: empty_pr_bucket_counts() for buyer in BUYERS}
    oc_by_buyer = {buyer: empty_oc_bucket_counts() for buyer in BUYERS}

    for row in rows:
        buyer = row["PGr"]
        manufacturer = blank_bucket(row["Manufactur"])
        is_uc4 = row["PO created by"] == "UC4CPIC"

        if is_uc4:
            overall_uc4 += 1

        by_buyer_counts[buyer]["total"] += 1
        by_manufacturer_counts[manufacturer]["total"] += 1
        if is_uc4:
            by_buyer_counts[buyer]["uc4_count"] += 1
            by_manufacturer_counts[manufacturer]["uc4_count"] += 1

        manufacturer_distribution[manufacturer] += 1
        if row["WBS element"] == "":
            wbs_distribution["blank_wbs"] += 1
        else:
            wbs_distribution["with_wbs"] += 1

        pr_bucket = expected_pr_bucket(row)
        oc_bucket = expected_oc_bucket(row)
        pr_buckets[pr_bucket] += 1
        oc_buckets[oc_bucket] += 1
        pr_by_buyer[buyer][pr_bucket] += 1
        oc_by_buyer[buyer][oc_bucket] += 1

    by_buyer = {}
    for buyer in BUYERS:
        counts = by_buyer_counts[buyer]
        by_buyer[buyer] = ratio_entry(counts["uc4_count"], counts["total"])

    by_manufacturer = {}
    for manufacturer in ["DummyMfr-X", "DummyMfr-Y", "DummyMfr-Z", "<BLANK>"]:
        counts = by_manufacturer_counts[manufacturer]
        by_manufacturer[manufacturer] = ratio_entry(counts["uc4_count"], counts["total"])

    return {
        "row_count": len(rows),
        "seed": SEED,
        "auto_po_ratio": {
            "overall": ratio_entry(overall_uc4, len(rows)),
            "by_buyer": by_buyer,
            "by_manufacturer": by_manufacturer,
        },
        "manufacturer_distribution": manufacturer_distribution,
        "wbs_distribution": wbs_distribution,
        "pr_lead_time": {
            "buckets": pr_buckets,
            "by_buyer": pr_by_buyer,
        },
        "oc_lead_time": {
            "buckets": oc_buckets,
            "by_buyer": oc_by_buyer,
        },
    }


def write_csv(rows):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def write_json(expected):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(expected, f, ensure_ascii=False, indent=2)
        f.write("\n")


def row_reference(index):
    doc_no, item = make_doc_item(index)
    return "Doc.No " + doc_no + " Item " + item


def write_readme(expected):
    blank_mfr_count = expected["manufacturer_distribution"]["<BLANK>"]
    blank_wbs_count = expected["wbs_distribution"]["blank_wbs"]
    uc4_count = expected["auto_po_ratio"]["overall"]["uc4_count"]
    readme = """# Dummy PO-Item Dataset

## Synthetic data only

This fixture is synthetic and must never be replaced with real company data. It lives under `data/dummy/` according to specs 02 and 03. Supplier names, vendor codes, material numbers, manufacturers, prices, project strings, and dates are deliberately fake.

The generator is `tests/fixtures/generate_dummy_po_items.py`. It writes exactly 300 PO-item rows to `data/dummy/dummy_po_items.csv` and independently computed ground truth to `data/dummy/dummy_po_items_expected.json`.

## EVAL-017: ChatBI Manufacturer Blank Bucket Is Explicit

- Deliberately constructed rows: rows 1-12 have blank `Manufactur`; additional random-fill rows may also be blank.
- Expected outcome: the JSON uses the literal `<BLANK>` bucket in `manufacturer_distribution` and `auto_po_ratio.by_manufacturer`.
- Current expected count: `<BLANK>` manufacturer rows = """ + str(blank_mfr_count) + """.
- Worked example: """ + row_reference(0) + """ has blank `Manufactur` and `PO created by = UC4CPIC`, so it covers the explicit blank manufacturer bucket and the auto-PO numerator.

## EVAL-018: ChatBI WBS Blank Rows Are Allowed

- Deliberately constructed rows: rows 13-36 have blank `WBS element`; rows 37-72 have project-style WBS values.
- Expected outcome: `wbs_distribution.blank_wbs` and `wbs_distribution.with_wbs` in the JSON add up to 300.
- Current expected count: blank WBS rows = """ + str(blank_wbs_count) + """.
- Worked example: """ + row_reference(12) + """ has blank `WBS element`, proving non-project rows are valid fixture records.

## EVAL-019: Auto PO Ratio Uses UC4CPIC Over All PO Items

- Deliberately constructed rows: rows 1-72 alternate `UC4CPIC`, `ZUSER1`, and `ZUSER2` across multiple buyers and manufacturers.
- Expected outcome: `auto_po_ratio.overall`, `auto_po_ratio.by_buyer`, and `auto_po_ratio.by_manufacturer` show both numerator and denominator.
- Current expected count: UC4 rows = """ + str(uc4_count) + """ out of 300.
- Worked example: """ + row_reference(1) + """ is a non-UC4 row and remains in the denominator for every matching filter context.

## EVAL-020: Lead Time Metrics Identify PR Versus OC Logic

- Deliberately constructed rows: the first 8 lead-time templates cover every PR bucket and every OC bucket; rows 5-7 are delivered-without-OC examples.
- Expected outcome: `pr_lead_time.buckets` contains `0<=X<=3`, `3<X<=7`, `>7days`, and `not statistic`; `oc_lead_time.buckets` contains `<=3`, `3<X<=7`, `>7`, `no order confirmation`, and `Delivered without OC`.
- Worked example: """ + row_reference(4) + """ has blank `PR Date`, blank `order confirmatioin date`, and populated `GR-D.o.Post`, so it covers PR `not statistic` and OC `Delivered without OC`.
"""
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)


def check_ratio_entry(entry):
    if entry["total"] == 0:
        return entry["ratio"] == 0.0
    return entry["ratio"] == round(entry["uc4_count"] / entry["total"], 6)


def verify_outputs(rows, expected):
    checks = []
    checks.append(("exactly 300 rows written", len(rows) == ROW_COUNT))
    checks.append(("Doc.No. and Item pairs are unique", len({(row["Doc. No."], row["Item"]) for row in rows}) == len(rows)))
    checks.append(("every PR bucket has >= 1 row", all(expected["pr_lead_time"]["buckets"][bucket] >= 1 for bucket in PR_BUCKETS)))
    checks.append(("every OC bucket has >= 1 row", all(expected["oc_lead_time"]["buckets"][bucket] >= 1 for bucket in OC_BUCKETS)))
    checks.append(("blank Manufactur count >= 10", expected["manufacturer_distribution"]["<BLANK>"] >= 10))
    checks.append(("blank WBS count >= 20", expected["wbs_distribution"]["blank_wbs"] >= 20))
    uc4_count = expected["auto_po_ratio"]["overall"]["uc4_count"]
    checks.append(("UC4CPIC count >= 1 and < 300", 1 <= uc4_count < ROW_COUNT))
    required_values_present = all(
        row[field] != ""
        for row in rows
        for field in ["Doc. No.", "Item", "PGr", "Vendor", "Doc. Date"]
    )
    checks.append(("no blank values in Doc. No., Item, PGr, Vendor, Doc. Date", required_values_present))

    ratios_ok = check_ratio_entry(expected["auto_po_ratio"]["overall"])
    for entry in expected["auto_po_ratio"]["by_buyer"].values():
        ratios_ok = ratios_ok and check_ratio_entry(entry)
    for entry in expected["auto_po_ratio"]["by_manufacturer"].values():
        ratios_ok = ratios_ok and check_ratio_entry(entry)

    totals_ok = (
        sum(expected["manufacturer_distribution"].values()) == ROW_COUNT
        and expected["wbs_distribution"]["with_wbs"] + expected["wbs_distribution"]["blank_wbs"] == ROW_COUNT
        and sum(expected["pr_lead_time"]["buckets"].values()) == ROW_COUNT
        and sum(expected["oc_lead_time"]["buckets"].values()) == ROW_COUNT
    )
    checks.append(("JSON ratios recompute correctly and bucket totals match", ratios_ok and totals_ok))

    failed = []
    for label, ok in checks:
        if ok:
            print("PASS " + label)
        else:
            print("FAIL " + label)
            failed.append(label)

    if failed:
        raise AssertionError("Generator acceptance checks failed: " + ", ".join(failed))


def main():
    rows = generate_rows()
    expected = compute_expected_stats(rows)
    write_csv(rows)
    write_json(expected)
    write_readme(expected)
    verify_outputs(rows, expected)


if __name__ == "__main__":
    main()
