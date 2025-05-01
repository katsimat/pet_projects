-- 2
SELECT DISTINCT
    r.name AS restaurant_name
FROM 
    db_rest.restaurant r
JOIN 
    db_rest.dishes_restaurant dr ON r.id_restaurant = dr.id_restaurant
JOIN 
    db_rest.dishes d ON dr.id_dishes = d.id_dishes
JOIN 
    db_rest.dishes_products dp ON d.id_dishes = dp.id_dishes
JOIN 
    db_rest.products p ON dp.id_products = p.id_products
WHERE 
    UPPER(p.name) NOT LIKE '%ЛУК%';