-- 3
SELECT 
    e.id_employees AS employee_id,
    e.firstname || ' ' || e.surname AS full_name,
    e.position,
    e.salary
FROM 
    db_rest.employees e
JOIN 
    db_rest.restaurant r ON e.id_restaurant = r.id_restaurant
WHERE 
    LOWER(r.name) = 'суши мастер';