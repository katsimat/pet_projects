-- 8
SELECT 
    p.name AS product_name,
    s.quality_assessment
FROM 
    db_rest.products p
JOIN 
    db_rest.supplier s ON p.id_supplier = s.id_supplier
ORDER BY 
    s.quality_assessment DESC
LIMIT 3;