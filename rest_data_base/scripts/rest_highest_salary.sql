-- 5
SELECT 
    r.name AS restaurant_name,
    e.salary AS max_waiter_salary
FROM 
    db_rest.employees e
JOIN 
    db_rest.restaurant r ON e.id_restaurant = r.id_restaurant
WHERE 
    LOWER(e.position) = 'официант'
ORDER BY 
    e.salary DESC
LIMIT 1;