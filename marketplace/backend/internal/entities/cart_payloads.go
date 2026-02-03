package entities

import "github.com/google/uuid"

type UpsertCartItemPayload struct {
	UserUID  uuid.UUID
	OfferUID uuid.UUID
	Quantity int
}

type UpsertCartItemResult = bool
