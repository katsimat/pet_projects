package queries

import _ "embed"

//go:embed upsert_cart_item.sql
var UpsertCartItem string

//go:embed delete_cart_item.sql
var DeleteCartItem string

//go:embed list_cart_items.sql
var ListCartItems string
