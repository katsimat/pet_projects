package cart

import (
	"context"
	"database/sql"
	"errors"
	"fmt"

	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"

	"github.com/katsimat/backend/internal/entities"
	cart_payloads "github.com/katsimat/backend/internal/repositories/cart/payloads"
	"github.com/katsimat/backend/internal/repositories/cart/queries"
)

type Repository struct {
	db *sqlx.DB
}

func NewRepository(db *sqlx.DB) *Repository {
	return &Repository{db: db}
}

func (r *Repository) GetLatestCartByUserUID(ctx context.Context, userUID uuid.UUID) (*uuid.UUID, *bool, error) {
	var cartUID uuid.UUID
	var isLocked bool
	if err := r.db.QueryRowxContext(ctx, "select uid, is_locked from cart where user_uid = $1 order by created_at desc limit 1", userUID).Scan(&cartUID, &isLocked); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, nil, nil
		}
		return nil, nil, err
	}
	return &cartUID, &isLocked, nil
}

func (r *Repository) UpsertItem(ctx context.Context, payload cart_payloads.UpsertCartItemPayload) error {
	stmt, err := r.db.PrepareNamedContext(ctx, queries.UpsertCartItem)
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.ExecContext(ctx, payload)
	return err
}

func (r *Repository) DeleteItem(ctx context.Context, cartUID uuid.UUID, offerUID uuid.UUID) (bool, error) {
	res, err := r.db.ExecContext(ctx, queries.DeleteCartItem, cartUID, offerUID)
	if err != nil {
		return false, fmt.Errorf("failed to delete cart item: %w", err)
	}
	affected, err := res.RowsAffected()
	if err != nil {
		return false, err
	}
	return affected > 0, nil
}

func (r *Repository) ListItems(ctx context.Context, cartUID uuid.UUID) ([]entities.CartItem, error) {
	rows, err := r.db.QueryxContext(ctx, queries.ListCartItems, cartUID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	items := make([]entities.CartItem, 0)
	for rows.Next() {
		var item entities.CartItem
		if err := rows.Scan(&item.OfferUID, &item.Quantity); err != nil {
			return nil, err
		}
		items = append(items, item)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return items, nil
}
