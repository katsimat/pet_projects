<details>
<summary><b>restaurant</b></summary>

|   | restaurant (ресторан)                       |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id_restaurant                               | id ресторана                                  | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | name                                        | название                                      | VARCHAR(200)  |             | NOT NULL |                                                                                                   |                           |
|   | opening_date                                | дата открытия                                 | TIMESTAMP     |             | NOT NULL | CHECK(opening_date <= CURRENT_TIMESTAMP)                                                          | DEFAULT CURRENT_TIMESTAMP |
|   | open_time                                   | время открытия (время работы)                 | TIME          |             | NOT NULL |                                                                                                   |                           |
|   | close_time                                  | время закрытия (время работы)                 | TIME          |             | NOT NULL | CHECK(close_time > open_time)                                                                     |                           |
|   | markup                                      | коэффициент наценки на блюдо                  | DECIMAL(10,2) |             | NOT NULL | CHECK(markup > 0)                                                                                 |                           |
|   | city                                        | город                                         | VARCHAR(200)  |             | NOT NULL |                                                                                                   |                           |
|   | street                                      | улица                                         | VARCHAR(200)  |             | NOT NULL |                                                                                                   |                           |
|   | house                                       | дом                                           | INTEGER       |             |          |                                                                                                   |                           |

</details>

<details>
<summary><b>employees</b></summary>

|   | employees (работники)                       |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id_employees                                | id работника                                  | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | firstname                                   | имя                                           | VARCHAR(100)  |             | NOT NULL |                                                                                                   |                           |
|   | surname                                     | фамилия                                       | VARCHAR(100)  |             | NOT NULL |                                                                                                   |                           |
|   | position                                    | должность                                     | VARCHAR(100)  |             | NOT NULL |                                                                                                   |                           |
|   | id_restaurant                               | id ресторана                                  | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | salary                                      | зарплата                                      | INTEGER       |             | NOT NULL | CHECK(salary >= 0)                                                                                | DEFAULT 0                 |
|   | bonus_salary                                | чаевые и другие надбавки                      | DECIMAL(10,2) |             | NOT NULL | CHECK(bonus_salary >= 0)                                                                          | DEFAULT 0                 |

</details>

<details>
<summary><b>dishes_restaurant</b></summary>

|   | dishes_restaurant (блюдо в ресторане)       |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id                                          | идентификатор                                 | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | id_restaurant                               | id ресторана                                  | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | id_dishes                                   | id блюда                                      | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | price_in_rest                               | цена в ресторане                              | DECIMAL(10,2) |             | NOT NULL | CHECK(price_in_rest >= 0)                                                                         |                           |

</details>

<details>
<summary><b>dishes</b></summary>

|   | dishes (блюда)                              |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id_dishes                                   | id блюда                                      | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | name                                        | название                                      | VARCHAR(100)  |             | NOT NULL |                                                                                                   |                           |
|   | cuisine                                     | блюдо какой кухни                             | VARCHAR(100)  |             |          |                                                                                                   |                           |
|   | price                                       | цена без наценки                              | DECIMAL(10,2) |             | NOT NULL | CHECK(price >= 0)                                                                                 |                           |

</details>

<details>
<summary><b>dishes_order</b></summary>

|   | dishes_order (блюдо в заказе)               |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id                                          | идентификатор                                 | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | id_dishes                                   | id блюда                                      | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | id_order                                    | id заказа                                     | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | cnt_items                                   | количество блюд с этим наименованием в заказе | INTEGER       |             | NOT NULL | CHECK(cnt_items >= 0)                                                                             | DEFAULT 1                 |

</details>

<details>
<summary><b>dishes_products</b></summary>

|   | dishes_products (продукт в блюде)           |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id                                          | идентификатор                                 | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | id_dishes                                   | id блюда                                      | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | id_products                                 | id продукта                                   | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | weight_product                              | вес продукта в блюде по рецепту               | DECIMAL(10,2) |             | NOT NULL | CHECK(weight_product >= 0)                                                                        | DEFAULT 0                 |

</details>

<details>
<summary><b>products</b></summary>

|   | products (продукты)                         |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id_products                                 | id продукта                                   | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | name                                        | наименование                                  | VARCHAR(100)  |             | NOT NULL |                                                                                                   |                           |
|   | price                                       | цена без наценки                              | DECIMAL(10,2) |             | NOT NULL | CHECK(price >= 0)                                                                                 |                           |
|   | id_supplier                                 | id поставщика                                 | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |

</details>

<details>
<summary><b>history_products</b></summary>

|   | history_products (версионирование продукты) |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id_products                                 | id продукта                                   | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | name                                        | наименование                                  | VARCHAR(100)  |             | NOT NULL |                                                                                                   |                           |
|   | price                                       | цена без наценки                              | DECIMAL(10,2) |             | NOT NULL | CHECK(price >= 0)                                                                                 |                           |
|   | id_supplier                                 | id поставщика                                 | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | from_dt                                     | актуальность цены с даты                      | TIMESTAMP     |             | NOT NULL | CHECK(from_dt <= CURRENT_TIMESTAMP)                                                               |                           |
|   | to_dt                                       | актуальность цены по дату                     | TIMESTAMP     |             | NOT NULL | CHECK(to_dt > from_dt)                                                                            |                           |

</details>

<details>
<summary><b>supplier</b></summary>

|   | supplier (поставщик)                        |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id_supplier                                 | id поставщика                                 | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | name                                        | название компании                             | VARCHAR(200)  |             | NOT NULL |                                                                                                   |                           |
|   | city                                        | город                                         | VARCHAR(200)  |             | NOT NULL |                                                                                                   |                           |
|   | street                                      | улица                                         | VARCHAR(200)  |             | NOT NULL |                                                                                                   |                           |
|   | house                                       | дом                                           | INTEGER       |             |          |                                                                                                   |                           |
|   | quality_assessment                          | надежность поставщика (оценка качества)       | DECIMAL(10,2) |             |          |                                                                                                   |                           |

</details>

<details>
<summary><b>orders</b></summary>

|   | orders (заказ)                               |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id_order                                    | id заказ                                      | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | id_customer                                 | id посетителя                                 | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | id_employees                                | id официанта (сотрудника)                     | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | id_restaurant                               | id ресторана                                  | INTEGER       | FOREIGN KEY | NOT NULL |                                                                                                   |                           |
|   | status                                      | стастус заказа                                | VARCHAR(40)   |             | NOT NULL | CHECK (status IN ('new', 'pending_payment', 'paid', 'preparing', 'ready', 'served', 'cancelled')) |                           |
|   | updated_at                                  | когда произошло обновление статуса            | TIMESTAMP     |             | NOT NULL |                                                                                                   |                           |
|   | payment_type                                | тип оплаты                                    | VARCHAR(40)   |             | NOT NULL | CHECK (payment_type IN ('cash', 'card', 'contactless', 'qr_code', 'loyalty_points'))              |                           |
|   | total_amount                                | сумма заказа                                  | DECIMAL(10,2) |             | NOT NULL | CHECK(total_amount >= 0)                                                                          |                           |

</details>

<details>
<summary><b>customer</b></summary>

|   | customer (посетитель)                       |                                               |               |             |          |                                                                                                   |                           |
|---|---------------------------------------------|-----------------------------------------------|---------------|-------------|----------|---------------------------------------------------------------------------------------------------|---------------------------|
|   | название                                    | описание                                      | тип данных    | KEY         | NOT NULL | CHECK                                                                                             | DEFAULT                   |
|   | id_customer                                 | id посетителя                                 | INTEGER       | PRIMARY KEY | NOT NULL |                                                                                                   |                           |
|   | name                                        | имя (никнейм)                                 | VARCHAR(100)  |             | NOT NULL |                                                                                                   | DEFAULT 'guest'           |
|   | bonus                                       | бонусные баллы                                | INTEGER       |             | NOT NULL | CHECK(bonus >= 0)                                                                                 |                           |
|   | registration_time                           | время регистрации в система                   | TIMESTAMP     |             | NOT NULL |                                                                                                   | DEFAULT CURRENT_TIMESTAMP |

</details>


