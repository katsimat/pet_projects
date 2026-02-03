package domain_errors

import "errors"

var ErrCartNotFound = errors.New("cart not found")

var ErrCartLocked = errors.New("cart is locked")

var ErrCartItemNotFound = errors.New("cart item not found")
