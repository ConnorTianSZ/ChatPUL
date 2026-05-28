from datetime import date, timedelta


PR_BUCKETS = ("0<=X<=3", "3<X<=7", ">7days", "not statistic")
OC_BUCKETS = ("<=3", "3<X<=7", ">7", "no order confirmation", "Delivered without OC")


def parse_date(value: str) -> date | None:
    if value == "":
        return None
    year, month, day = value.split("-")
    return date(int(year), int(month), int(day))


def networkdays(start: date, end: date) -> int:
    current = start
    total = 0
    while current <= end:
        if current.weekday() < 5:
            total += 1
        current += timedelta(days=1)
    return total


def pr_lead_time_bucket(row: dict[str, str]) -> str:
    pr_date = parse_date(row["PR Date"])
    doc_date = parse_date(row["Doc. Date"])
    if pr_date is None or doc_date is None:
        return "not statistic"

    lead_time = networkdays(pr_date, doc_date) - 1
    if 0 <= lead_time <= 3:
        return "0<=X<=3"
    if 3 < lead_time <= 7:
        return "3<X<=7"
    if lead_time > 7:
        return ">7days"
    return "not statistic"


def po_confirmation_lead_time_bucket(row: dict[str, str]) -> str:
    order_confirmation_date = parse_date(row["order confirmatioin date"])
    if order_confirmation_date is None:
        if row["GR-D.o.Post"] != "":
            return "Delivered without OC"
        return "no order confirmation"

    doc_date = parse_date(row["Doc. Date"])
    if doc_date is None:
        return "no order confirmation"

    lead_time = networkdays(doc_date, order_confirmation_date) - 1
    if lead_time <= 3:
        return "<=3"
    if 3 < lead_time <= 7:
        return "3<X<=7"
    return ">7"


def empty_pr_buckets() -> dict[str, int]:
    return {bucket: 0 for bucket in PR_BUCKETS}


def empty_oc_buckets() -> dict[str, int]:
    return {bucket: 0 for bucket in OC_BUCKETS}
