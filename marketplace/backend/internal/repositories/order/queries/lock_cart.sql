update cart
set is_locked = true
where uid = $1 and is_locked = false
