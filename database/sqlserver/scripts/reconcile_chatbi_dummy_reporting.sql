SELECT
    COUNT_BIG(*) AS row_count,
    SUM(CASE WHEN po_created_by = N'UC4CPIC' THEN 1 ELSE 0 END) AS uc4_count,
    SUM(CASE WHEN manufacturer_name IS NULL OR manufacturer_name = N'' THEN 1 ELSE 0 END) AS blank_manufacturer_count,
    SUM(CASE WHEN wbs_element IS NULL OR wbs_element = N'' THEN 1 ELSE 0 END) AS blank_wbs_count
FROM chatbi.vw_po_item_reporting;

SELECT
    COALESCE(NULLIF(manufacturer_name, N''), N'<BLANK>') AS manufacturer_bucket,
    COUNT_BIG(*) AS po_item_count
FROM chatbi.vw_po_item_reporting
GROUP BY COALESCE(NULLIF(manufacturer_name, N''), N'<BLANK>')
ORDER BY manufacturer_bucket;

SELECT
    buyer_key,
    COUNT_BIG(*) AS total,
    SUM(CASE WHEN po_created_by = N'UC4CPIC' THEN 1 ELSE 0 END) AS uc4_count
FROM chatbi.vw_po_item_reporting
GROUP BY buyer_key
ORDER BY buyer_key;
