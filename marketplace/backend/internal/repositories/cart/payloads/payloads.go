package payloads

import "github.com/google/uuid"

type UpsertCartItemPayload struct {
	CartUID  uuid.UUID `db:"cart_uid"`
	OfferUID uuid.UUID `db:"offer_uid"`
	Quantity int       `db:"quantity"`
}
