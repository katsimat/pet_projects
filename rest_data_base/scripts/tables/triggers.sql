CREATE OR REPLACE FUNCTION update_history_products() RETURNS TRIGGER AS $$
    BEGIN
        UPDATE db_rest.history_products
        SET to_dt = CURRENT_TIMESTAMP
        WHERE id_products = OLD.id_products AND to_dt = '9999-12-31 23:59:59';

        INSERT INTO db_rest.history_products (id_products, name, price, id_supplier, from_dt)
        VALUES (
            NEW.id_products, NEW.name, NEW.price, NEW.id_supplier, CURRENT_TIMESTAMP
        );

        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tg_update_history_products
    AFTER UPDATE OR DELETE ON db_rest.products
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.* OR NEW.* IS NULL)
EXECUTE FUNCTION update_history_products();


-----------------------------------------------------
CREATE OR REPLACE FUNCTION update_dish_price() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE db_rest.dishes
    SET price = (
        SELECT SUM(p.price * dp.weight_product)
        FROM db_rest.dishes_products dp
        JOIN db_rest.products p ON dp.id_products = p.id_products
        WHERE dp.id_dishes = dishes.id_dishes
    )
    WHERE dishes.id_dishes IN (
        SELECT dp.id_dishes
        FROM db_rest.dishes_products dp
        WHERE dp.id_products = NEW.id_products
    );

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tg_update_dish_price
    AFTER UPDATE ON db_rest.products
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
EXECUTE FUNCTION update_dish_price();

--------------------------------------------------------
CREATE OR REPLACE FUNCTION update_price_in_rest()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE db_rest.dishes_restaurant
    SET price_in_rest = NEW.price * r.markup
    FROM db_rest.restaurant r
    WHERE dishes_restaurant.id_dishes = NEW.id_dishes
    AND dishes_restaurant.id_restaurant = r.id_restaurant;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER tg_update_price_in_rest
    AFTER UPDATE ON db_rest.dishes
    FOR EACH ROW
    WHEN (OLD.* IS DISTINCT FROM NEW.*)
EXECUTE FUNCTION update_price_in_rest();


analyze
UPDATE db_rest.products
SET price = 1000.00
WHERE id_products = 1;

