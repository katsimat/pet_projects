-- 6
SELECT 
    c.name AS customer_name,
    o.id_order AS order_id,
    o.total_amount,
    o.updated_at
FROM 
    db_rest.customer c
JOIN 
    db_rest.orders o ON c.id_customer = o.id_customer
WHERE 
    o.status = 'new';