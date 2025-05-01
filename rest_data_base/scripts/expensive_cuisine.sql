-- 9
SELECT 
    d.cuisine,
    d.name,
    d.price AS max_price
FROM 
    db_rest.dishes d
ORDER BY 
    d.price DESC
LIMIT 1;
