DROP SCHEMA db_rest CASCADE;
CREATE SCHEMA db_rest;
SET search_path TO db_rest,public;

CREATE TABLE restaurant (
    id_restaurant SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    opening_date TIMESTAMP CHECK(opening_date <= CURRENT_TIMESTAMP) DEFAULT CURRENT_TIMESTAMP,
    open_time TIME NOT NULL,
    close_time TIME NOT NULL CHECK(close_time > open_time),
    markup DECIMAL(10,2) NOT NULL CHECK(markup > 0),
    city VARCHAR(200) NOT NULL,
    street VARCHAR(200) NOT NULL,
    house INTEGER
);

CREATE TABLE supplier (
    id_supplier SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    city VARCHAR(200) NOT NULL,
    street VARCHAR(200) NOT NULL,
    house INTEGER,
    quality_assessment DECIMAL(10,2)
);

CREATE TABLE products (
    id_products SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK(price >= 0),
    id_supplier INTEGER NOT NULL,
    FOREIGN KEY (id_supplier) REFERENCES supplier(id_supplier)
);

CREATE TABLE history_products (
    id_history SERIAL,
    id_products INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK(price >= 0),
    id_supplier INTEGER NOT NULL,
    from_dt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP CHECK(from_dt <= CURRENT_TIMESTAMP),
    to_dt TIMESTAMP CHECK(to_dt > from_dt) DEFAULT '9999-12-31 23:59:59',
    PRIMARY KEY (id_products, from_dt),
    FOREIGN KEY (id_supplier) REFERENCES supplier(id_supplier)
);

CREATE TABLE dishes (
    id_dishes SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cuisine VARCHAR(100),
    price DECIMAL(10,2) NOT NULL CHECK(price >= 0)
);

CREATE TABLE dishes_products (
    id SERIAL PRIMARY KEY,
    id_dishes INTEGER NOT NULL,
    id_products INTEGER NOT NULL,
    weight_product DECIMAL(10,2) NOT NULL CHECK(weight_product >= 0) DEFAULT 0,
    FOREIGN KEY (id_dishes) REFERENCES dishes(id_dishes),
    FOREIGN KEY (id_products) REFERENCES products(id_products)
);

CREATE TABLE dishes_restaurant (
    id SERIAL PRIMARY KEY,
    id_restaurant INTEGER NOT NULL,
    id_dishes INTEGER NOT NULL,
    price_in_rest DECIMAL(10,2) NOT NULL CHECK(price_in_rest >= 0),
    FOREIGN KEY (id_restaurant) REFERENCES restaurant(id_restaurant),
    FOREIGN KEY (id_dishes) REFERENCES dishes(id_dishes)
);

CREATE TABLE customer (
    id_customer SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL DEFAULT 'guest',
    bonus INTEGER NOT NULL CHECK(bonus >= 0),
    registration_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employees (
    id_employees SERIAL PRIMARY KEY,
    firstname VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    id_restaurant INTEGER NOT NULL,
    salary INTEGER NOT NULL CHECK(salary >= 0) DEFAULT 0,
    bonus_salary DECIMAL(10,2) NOT NULL CHECK(bonus_salary >= 0) DEFAULT 0,
    FOREIGN KEY (id_restaurant) REFERENCES restaurant(id_restaurant)
);

CREATE TABLE orders (
    id_order SERIAL PRIMARY KEY,
    id_customer INTEGER NOT NULL,
    id_employees INTEGER NOT NULL,
    id_restaurant INTEGER NOT NULL,
    status VARCHAR(40) NOT NULL CHECK (status IN ('new', 'pending_payment', 'paid', 'preparing', 'ready', 'served', 'cancelled')),
    updated_at TIMESTAMP NOT NULL,
    payment_type VARCHAR(40) NOT NULL CHECK (payment_type IN ('cash', 'card', 'contactless', 'qr_code', 'loyalty_points')),
    total_amount DECIMAL(10,2) NOT NULL CHECK(total_amount >= 0),
    FOREIGN KEY (id_customer) REFERENCES customer(id_customer),
    FOREIGN KEY (id_employees) REFERENCES employees(id_employees),
    FOREIGN KEY (id_restaurant) REFERENCES restaurant(id_restaurant)
);

CREATE TABLE dishes_order (
    id SERIAL PRIMARY KEY,
    id_dishes INTEGER NOT NULL,
    id_order INTEGER NOT NULL,
    cnt_items INTEGER NOT NULL CHECK(cnt_items >= 0) DEFAULT 1,
    FOREIGN KEY (id_dishes) REFERENCES dishes(id_dishes),
    FOREIGN KEY (id_order) REFERENCES orders(id_order)
);