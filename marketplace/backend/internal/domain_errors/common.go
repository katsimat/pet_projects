package domain_errors

import "errors"

var ErrUserNotFound = errors.New("user not found")

var ErrInvalidPassword = errors.New("invalid password")
