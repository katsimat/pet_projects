-- 11
SELECT
    r.name AS restaurant_name,
    d.name AS dishes_name
FROM
    db_rest.restaurant r
JOIN
    db_rest.dishes_restaurant dr ON dr.id_restaurant = r.id_restaurant
JOIN
    db_rest.dishes d ON dr.id_dishes = d.id_dishes
WHERE
    LOWER(d.cuisine) LIKE '%итальянск%';
