CREATE INDEX ind_dish_order_order ON db_rest.dishes_order(id_order);
CREATE INDEX ind_dish_order_dish ON db_rest.dishes_order(id_dishes);
CREATE INDEX ind_dish_prod_prod ON db_rest.dishes_products(id_products);
CREATE INDEX ind_dish_prod_dish ON db_rest.dishes_products(id_dishes);

DROP INDEX IF EXISTS db_rest.ind_dish_order_order;
DROP INDEX IF EXISTS db_rest.ind_dish_order_dish;
DROP INDEX IF EXISTS db_rest.ind_dish_prod_prod;
DROP INDEX IF EXISTS db_rest.ind_dish_prod_dish;

--SELECT indexname, indexdef 
--FROM pg_indexes 
--WHERE tablename = 'dishes_order';
