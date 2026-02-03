do $$
declare
    seller_uid uuid;
    buyer_uid  uuid;
    buyer_cart_uid uuid;
begin
    insert into users (email, name, surname, password, role)
    values ('seller_mvp@example.com', 'Seller', 'User', 'sellerpass', 'seller')
    on conflict (email) do update
    set name = excluded.name,
        surname = excluded.surname,
        password = excluded.password,
        role = excluded.role
    returning uid into seller_uid;

    insert into users (email, name, surname, password, role)
    values ('buyer_mvp@example.com', 'Buyer', 'User', 'buyerpass', 'buyer')
    on conflict (email) do update
    set name = excluded.name,
        surname = excluded.surname,
        password = excluded.password,
        role = excluded.role
    returning uid into buyer_uid;

    select uid into buyer_cart_uid
    from cart
    where user_uid = buyer_uid
      and is_locked = false
    order by created_at desc
    limit 1;

    if buyer_cart_uid is null then
        insert into cart (user_uid, is_locked)
        values (buyer_uid, false)
        returning uid into buyer_cart_uid;
    end if;

    insert into offer (uid, seller_uid, title, description, price, quantity, status)
    values ('11111111-1111-1111-1111-111111111111', seller_uid, 'Apple iPhone', 'brand new', '10.00', 5, 'active')
    on conflict (uid) do update
    set seller_uid = excluded.seller_uid,
        title = excluded.title,
        description = excluded.description,
        price = excluded.price,
        quantity = excluded.quantity,
        status = excluded.status;

    insert into offer (uid, seller_uid, title, description, price, quantity, status)
    values ('22222222-2222-2222-2222-222222222222', seller_uid, 'Apple Banana', 'hidden', '11.00', 5, 'inactive')
    on conflict (uid) do update
    set seller_uid = excluded.seller_uid,
        title = excluded.title,
        description = excluded.description,
        price = excluded.price,
        quantity = excluded.quantity,
        status = excluded.status;

    insert into offer (uid, seller_uid, title, description, price, quantity, status)
    values ('33333333-3333-3333-3333-333333333333', seller_uid, 'MacBook Pro', 'laptop', '1500.00', 2, 'active')
    on conflict (uid) do update
    set seller_uid = excluded.seller_uid,
        title = excluded.title,
        description = excluded.description,
        price = excluded.price,
        quantity = excluded.quantity,
        status = excluded.status;

    insert into offer (uid, seller_uid, title, description, price, quantity, status)
    values ('44444444-4444-4444-4444-444444444444', seller_uid, 'Mechanical Keyboard', 'clicky', '120.00', 7, 'active')
    on conflict (uid) do update
    set seller_uid = excluded.seller_uid,
        title = excluded.title,
        description = excluded.description,
        price = excluded.price,
        quantity = excluded.quantity,
        status = excluded.status;

    insert into offer (uid, seller_uid, title, description, price, quantity, status)
    values ('55555555-5555-5555-5555-555555555555', seller_uid, 'Headphones', 'noise cancelling', '199.99', 9, 'active')
    on conflict (uid) do update
    set seller_uid = excluded.seller_uid,
        title = excluded.title,
        description = excluded.description,
        price = excluded.price,
        quantity = excluded.quantity,
        status = excluded.status;

    insert into offer (uid, seller_uid, title, description, price, quantity, status)
    values ('66666666-6666-6666-6666-666666666666', seller_uid, 'Coffee Beans', '1kg', '18.50', 25, 'active')
    on conflict (uid) do update
    set seller_uid = excluded.seller_uid,
        title = excluded.title,
        description = excluded.description,
        price = excluded.price,
        quantity = excluded.quantity,
        status = excluded.status;

    insert into offer (uid, seller_uid, title, description, price, quantity, status)
    values ('77777777-7777-7777-7777-777777777777', seller_uid, 'Notebook', 'paper', '4.99', 100, 'active')
    on conflict (uid) do update
    set seller_uid = excluded.seller_uid,
        title = excluded.title,
        description = excluded.description,
        price = excluded.price,
        quantity = excluded.quantity,
        status = excluded.status;

end;
$$ language 'plpgsql';


