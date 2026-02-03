package queries

import _ "embed"

//go:embed create_order.sql
var CreateOrder string

//go:embed lock_cart.sql
var LockCart string

//go:embed create_cart.sql
var CreateCart string
