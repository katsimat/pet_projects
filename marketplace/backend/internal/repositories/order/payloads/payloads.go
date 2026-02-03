package payloads

import (
	"github.com/google/uuid"

	"github.com/katsimat/backend/internal/entities"
)

type CreateOrderPayload struct {
	UID     uuid.UUID            `db:"uid"`
	CartUID uuid.UUID            `db:"cart_uid"`
	Status  entities.OrderStatus `db:"status"`
}
