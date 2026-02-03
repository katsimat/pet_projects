create extension if not exists "uuid-ossp";

create domain email_address as varchar(255)
    check (value ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

create domain non_negative_decimal as decimal(10, 2)
    check (value >= 0);

create domain non_negative_integer as integer
    check (value >= 0);

create type user_role as enum ('buyer', 'seller', 'admin');
create type offer_status as enum ('active', 'inactive', 'sold_out');
create type order_status as enum ('pending', 'confirmed', 'delivering', 'completed', 'cancelled');

create table if not exists users (
    uid              uuid                        primary key default uuid_generate_v4(),
    email            email_address               not null unique,
    name             varchar(255)                not null,
    surname          varchar(255)                not null,
    password         varchar(255)                not null,
    role             user_role                   not null,
    created_at       timestamp with time zone    not null default now(),
    updated_at       timestamp with time zone    not null default now()
);

create table if not exists offer (
    uid              uuid                        primary key default uuid_generate_v4(),
    seller_uid       uuid                        not null references users(uid) on delete cascade,
    title            varchar(255)                not null,
    description      text,
    price            non_negative_decimal        not null,
    quantity         non_negative_integer        not null,
    status           offer_status                not null,
    created_at       timestamp with time zone    not null default now(),
    updated_at       timestamp with time zone    not null default now()
);
create index if not exists offer_ix_seller_uid on offer(seller_uid);

create table if not exists cart (
    uid              uuid                        primary key default uuid_generate_v4(),
    user_uid         uuid                        not null references users(uid) on delete cascade,
    is_locked        boolean                     not null default false,
    created_at       timestamp with time zone    not null default now(),
    updated_at       timestamp with time zone    not null default now()
);
create index if not exists cart_ix_user_uid on cart(user_uid);
create unique index if not exists cart_uix_user_uid_unlocked on cart(user_uid) where is_locked = false;

create table if not exists cart_item (
    cart_uid         uuid                        not null references cart(uid) on delete cascade,
    offer_uid        uuid                        not null references offer(uid) on delete cascade,
    quantity         integer                     not null check (quantity > 0),
    created_at       timestamp with time zone    not null default now(),
    updated_at       timestamp with time zone    not null default now(),
    primary key (cart_uid, offer_uid)
);

create table if not exists orders (
    uid              uuid                        primary key default uuid_generate_v4(),
    cart_uid         uuid                        not null references cart(uid) on delete restrict,
    status           order_status                not null,
    created_at       timestamp with time zone    not null default now(),
    updated_at       timestamp with time zone    not null default now()
);
create index if not exists orders_ix_cart_uid on orders(cart_uid);

create or replace function create_cart_for_new_user()
returns trigger as $$
begin
    insert into cart (user_uid, is_locked)
    values (new.uid, false);
    return new;
end;
$$ language 'plpgsql';

drop trigger if exists create_cart_for_new_user_trigger on users;
create trigger create_cart_for_new_user_trigger after insert on users
    for each row execute function create_cart_for_new_user();

create or replace function update_updated_at_column()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language 'plpgsql';

drop trigger if exists update_user_updated_at on users;
create trigger update_user_updated_at before update on users
    for each row execute function update_updated_at_column();

drop trigger if exists update_offer_updated_at on offer;
create trigger update_offer_updated_at before update on offer
    for each row execute function update_updated_at_column();

drop trigger if exists update_cart_updated_at on cart;
create trigger update_cart_updated_at before update on cart
    for each row execute function update_updated_at_column();

drop trigger if exists update_cart_item_updated_at on cart_item;
create trigger update_cart_item_updated_at before update on cart_item
    for each row execute function update_updated_at_column();

drop trigger if exists update_order_updated_at on orders;
create trigger update_order_updated_at before update on orders
    for each row execute function update_updated_at_column();
