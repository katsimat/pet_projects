package entities

import (
	"github.com/google/uuid"
)

type UserCredentials struct {
	UID      uuid.UUID `db:"uid"`
	Email    string    `db:"email"`
	Password string    `db:"password"`
}

type LoginPayload struct {
	Email    string
	Password string
}

type LoginResult struct {
	UID   string
	Email string
}
