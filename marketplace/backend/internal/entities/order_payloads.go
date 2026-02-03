package entities

import "github.com/google/uuid"

type CreateOrderPayload struct {
	UserUID uuid.UUID
}

type CreateOrderResult = Order
