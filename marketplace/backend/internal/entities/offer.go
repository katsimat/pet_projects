package entities

import (
	"time"

	"github.com/google/uuid"
)

type OfferStatus string

const (
	OfferStatusActive   OfferStatus = "active"
	OfferStatusInactive OfferStatus = "inactive"
	OfferStatusSoldOut  OfferStatus = "sold_out"
)

type Offer struct {
	UID           uuid.UUID   `db:"uid"`
	SellerUID     uuid.UUID   `db:"seller_uid"`
	SellerEmail   string      `db:"seller_email"`
	SellerName    string      `db:"seller_name"`
	SellerSurname string      `db:"seller_surname"`
	Title         string      `db:"title"`
	Description   *string     `db:"description"`
	Price         string      `db:"price"`
	Quantity      int         `db:"quantity"`
	Status        OfferStatus `db:"status"`
	CreatedAt     time.Time   `db:"created_at"`
	UpdatedAt     time.Time   `db:"updated_at"`
}
