select
    offer_uid,
    quantity
from cart_item
where cart_uid = $1
order by created_at asc;
