package offer

import (
	"context"
	"database/sql"
	"errors"

	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"

	"github.com/katsimat/backend/internal/entities"
	"github.com/katsimat/backend/internal/repositories/offer/queries"
)

type Repository struct {
	db *sqlx.DB
}

func NewRepository(db *sqlx.DB) *Repository {
	return &Repository{db: db}
}

func (r *Repository) GetByUID(ctx context.Context, uid uuid.UUID) (*entities.Offer, error) {
	offer := &entities.Offer{}
	err := r.db.GetContext(ctx, offer, queries.GetByUID, uid)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, nil
		}
		return nil, err
	}
	return offer, nil
}

func (r *Repository) ListActiveBySearch(ctx context.Context, q string) ([]entities.Offer, error) {
	var offers []entities.Offer
	if err := r.db.SelectContext(ctx, &offers, queries.ListActiveBySearch, q); err != nil {
		return nil, err
	}
	return offers, nil
}
