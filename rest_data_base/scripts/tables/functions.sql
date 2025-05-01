CREATE OR REPLACE FUNCTION get_position(id INT) RETURNS VARCHAR(100) AS $$
BEGIN
    RETURN position FROM db_rest.employees WHERE id_employees = id; 
END;
$$ LANGUAGE plpgsql;

CREATE TYPE order_status AS ENUM ('new', 'pending_payment', 'paid', 'preparing', 'ready', 'served', 'cancelled');
CREATE OR REPLACE FUNCTION update_order_status(id INT) RETURNS VARCHAR AS $$
DECLARE
    next_status order_status;
    cur_status order_status;
    arr_status order_status[] = ARRAY['new', 'pending_payment', 'paid', 'preparing', 'ready', 'served', 'cancelled'];
BEGIN
    SELECT o.status INTO cur_status
    FROM db_rest.orders o
    WHERE o.id_order = id;

    IF cur_status IS NULL OR cur_status = 'cancelled' THEN
        RETURN 'ERROR';
    END IF;

    next_status := arr_status[array_position(arr_status, cur_status) + 1];

    UPDATE db_rest.orders 
    SET status = next_status, updated_at = CURRENT_TIMESTAMP
    WHERE id = id_order;
    RETURN next_status;
END;
$$ LANGUAGE plpgsql;
