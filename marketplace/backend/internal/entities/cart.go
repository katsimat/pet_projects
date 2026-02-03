package entities

import "github.com/google/uuid"

type CartItem struct {
	OfferUID uuid.UUID
	Quantity int
}

type GetCartPayload struct {
	UserUID uuid.UUID
}

type GetCartResult = []CartItem
