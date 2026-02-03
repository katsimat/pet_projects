insert into cart_item (cart_uid, offer_uid, quantity)
values (:cart_uid, :offer_uid, :quantity)
on conflict (cart_uid, offer_uid)
do update set quantity = excluded.quantity
