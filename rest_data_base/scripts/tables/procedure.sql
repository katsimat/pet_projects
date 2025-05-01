CREATE OR REPLACE PROCEDURE add_order(in id_cust INT, in id_emp INT, in id_rest INT, in payment_type VARCHAR(100) DEFAULT 'card') AS $$
    INSERT INTO db_rest.orders (
        id_customer,
        id_employees,
        id_restaurant,
        status,
        updated_at,
        payment_type,
        total_amount
    )
    VALUES(id_cust, id_emp, id_rest, 'new', CURRENT_TIMESTAMP, payment_type, 10000);
$$ LANGUAGE SQL;
