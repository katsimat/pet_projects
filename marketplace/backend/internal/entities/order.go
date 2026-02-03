package entities

import "github.com/google/uuid"

type OrderStatus string

const (
	OrderStatusPending    OrderStatus = "pending"
	OrderStatusConfirmed  OrderStatus = "confirmed"
	OrderStatusDelivering OrderStatus = "delivering"
	OrderStatusCompleted  OrderStatus = "completed"
	OrderStatusCancelled  OrderStatus = "cancelled"
)

type Order struct {
	UID     uuid.UUID   `db:"uid"`
	CartUID uuid.UUID   `db:"cart_uid"`
	Status  OrderStatus `db:"status"`
}
