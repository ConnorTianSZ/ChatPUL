# Dummy PO-Item Dataset

## Synthetic data only

This fixture is synthetic and must never be replaced with real company data. It lives under `data/dummy/` according to specs 02 and 03. Supplier names, vendor codes, material numbers, manufacturers, prices, project strings, and dates are deliberately fake.

The generator is `tests/fixtures/generate_dummy_po_items.py`. It writes exactly 300 PO-item rows to `data/dummy/dummy_po_items.csv` and independently computed ground truth to `data/dummy/dummy_po_items_expected.json`.

## EVAL-017: ChatBI Manufacturer Blank Bucket Is Explicit

- Deliberately constructed rows: rows 1-12 have blank `Manufactur`; additional random-fill rows may also be blank.
- Expected outcome: the JSON uses the literal `<BLANK>` bucket in `manufacturer_distribution` and `auto_po_ratio.by_manufacturer`.
- Current expected count: `<BLANK>` manufacturer rows = 50.
- Worked example: Doc.No 90000001 Item 00010 has blank `Manufactur` and `PO created by = UC4CPIC`, so it covers the explicit blank manufacturer bucket and the auto-PO numerator.

## EVAL-018: ChatBI WBS Blank Rows Are Allowed

- Deliberately constructed rows: rows 13-36 have blank `WBS element`; rows 37-72 have project-style WBS values.
- Expected outcome: `wbs_distribution.blank_wbs` and `wbs_distribution.with_wbs` in the JSON add up to 300.
- Current expected count: blank WBS rows = 100.
- Worked example: Doc.No 90000005 Item 00010 has blank `WBS element`, proving non-project rows are valid fixture records.

## EVAL-019: Auto PO Ratio Uses UC4CPIC Over All PO Items

- Deliberately constructed rows: rows 1-72 alternate `UC4CPIC`, `ZUSER1`, and `ZUSER2` across multiple buyers and manufacturers.
- Expected outcome: `auto_po_ratio.overall`, `auto_po_ratio.by_buyer`, and `auto_po_ratio.by_manufacturer` show both numerator and denominator.
- Current expected count: UC4 rows = 104 out of 300.
- Worked example: Doc.No 90000001 Item 00020 is a non-UC4 row and remains in the denominator for every matching filter context.

## EVAL-020: Lead Time Metrics Identify PR Versus OC Logic

- Deliberately constructed rows: the first 8 lead-time templates cover every PR bucket and every OC bucket; rows 5-7 are delivered-without-OC examples.
- Expected outcome: `pr_lead_time.buckets` contains `0<=X<=3`, `3<X<=7`, `>7days`, and `not statistic`; `oc_lead_time.buckets` contains `<=3`, `3<X<=7`, `>7`, `no order confirmation`, and `Delivered without OC`.
- Worked example: Doc.No 90000002 Item 00020 has blank `PR Date`, blank `order confirmatioin date`, and populated `GR-D.o.Post`, so it covers PR `not statistic` and OC `Delivered without OC`.
