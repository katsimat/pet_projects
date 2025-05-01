-- 7
INSERT INTO db_rest.orders (
    id_customer,
    id_employees,
    id_restaurant,
    status,
    updated_at,
    payment_type,
    total_amount
) VALUES (
    (SELECT id_customer FROM db_rest.customer WHERE name = 'Иван'),
    (SELECT id_employees FROM db_rest.employees WHERE firstname = 'Петр' AND surname = 'Петров' AND id_restaurant = 2),
    2,
    'new',
    CURRENT_TIMESTAMP,
    'card',
    1500.00
);