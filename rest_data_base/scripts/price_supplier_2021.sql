-- 4
explain
SELECT 
    p.name AS product_name,
    s.name AS supplier_name,
    hp.price AS price_2021
FROM 
    db_rest.history_products hp
JOIN 
    db_rest.products p ON hp.id_products = p.id_products
JOIN 
    db_rest.supplier s ON hp.id_supplier = s.id_supplier
WHERE 
    EXTRACT(YEAR FROM hp.from_dt) = 2021 OR EXTRACT(YEAR FROM hp.to_dt) = 2021;