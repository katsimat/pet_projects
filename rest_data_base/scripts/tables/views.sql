CREATE VIEW dishes_products_v AS
SELECT d.id_dishes
    , d.name AS dishes_name
    , p.name AS product_name
    , p.price AS product_price
FROM db_rest.dishes d
    JOIN db_rest.dishes_products dp ON d.id_dishes = dp.id_dishes
    JOIN db_rest.products p ON p.id_products = dp.id_products
;

CREATE VIEW waiter_rest_v AS
SELECT r.name AS rest_name
    , e.firstname
    , e.surname
    , e.salary
FROM
    db_rest.restaurant r
    JOIN db_rest.employees e
    ON e.id_restaurant = r.id_restaurant
WHERE LOWER(e.position) = 'waiter' OR LOWER(e.position) = 'официант';
