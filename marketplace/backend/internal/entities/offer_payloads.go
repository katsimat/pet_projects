package entities

import "github.com/google/uuid"

type GetOfferPayload struct {
	UID uuid.UUID
}

type GetOfferResult = Offer
