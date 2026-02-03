select
    o.uid,
    o.seller_uid,
    u.email   as seller_email,
    u.name    as seller_name,
    u.surname as seller_surname,
    o.title,
    o.description,
    o.price,
    o.quantity,
    o.status,
    o.created_at,
    o.updated_at
from offer as o
join users as u on u.uid = o.seller_uid
where o.status = 'active'
  and (
      $1 = '' or
      o.title ilike ('%' || $1 || '%') or
      coalesce(o.description, '') ilike ('%' || $1 || '%')
  )
order by o.created_at desc


