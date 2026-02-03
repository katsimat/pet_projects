drop trigger if exists update_order_updated_at on orders;
drop trigger if exists update_cart_item_updated_at on cart_item;
drop trigger if exists update_cart_updated_at on cart;
drop trigger if exists update_offer_updated_at on offer;
drop trigger if exists update_user_updated_at on users;
drop trigger if exists create_cart_for_new_user_trigger on users;

drop function if exists create_cart_for_new_user();
drop function if exists update_updated_at_column();

drop table if exists orders;
drop table if exists cart_item;
drop table if exists cart;
drop table if exists offer;
drop table if exists users;

drop type if exists order_status;
drop type if exists offer_status;
drop type if exists user_role;

drop domain if exists non_negative_integer;
drop domain if exists non_negative_decimal;
drop domain if exists email_address;
