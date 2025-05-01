-- 10
WITH ranked_dishes AS (
    SELECT 
        r.name AS restaurant_name,
        d.name AS dish_name,
        dr.price_in_rest,
        RANK() OVER (PARTITION BY r.id_restaurant ORDER BY dr.price_in_rest DESC) AS price_rank
    FROM 
        db_rest.dishes_restaurant dr
    JOIN 
        db_rest.restaurant r ON dr.id_restaurant = r.id_restaurant
    JOIN 
        db_rest.dishes d ON dr.id_dishes = d.id_dishes
)
SELECT 
    restaurant_name,
    dish_name,
    price_in_rest,
    price_rank
FROM 
    ranked_dishes
WHERE 
    price_rank <= 3
ORDER BY 
    restaurant_name, price_rank;