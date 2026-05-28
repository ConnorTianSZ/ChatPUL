# SQL Server Dummy Data

Development database fixtures live here.

Dummy data must not include real supplier names, prices, project details, internal report values, or confidential identifiers.

Current loader:

- `load_dummy_po_items.py`: loads `data/dummy/dummy_po_items.csv` into the dummy-only ChatBI SQL Server staging tables.
