package order

import (
	"context"
	"database/sql"
	"errors"

	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"

	"github.com/katsimat/backend/internal/repositories/order/payloads"
	"github.com/katsimat/backend/internal/repositories/order/queries"
)

type Repository struct {
	db *sqlx.DB
}

func NewRepository(db *sqlx.DB) *Repository {
	return &Repository{db: db}
}

func (r *Repository) WithTx(ctx context.Context, fn func(tx *sqlx.Tx) error) error {
	tx, err := r.db.BeginTxx(ctx, &sql.TxOptions{})
	if err != nil {
		return err
	}
	defer tx.Rollback()

	if err := fn(tx); err != nil {
		return err
	}
	return tx.Commit()
}

func (r *Repository) GetLatestCartByUserUID(ctx context.Context, tx *sqlx.Tx, userUID uuid.UUID) (*uuid.UUID, *bool, error) {
	var cartUID uuid.UUID
	var isLocked bool
	if err := tx.QueryRowxContext(ctx, "select uid, is_locked from cart where user_uid = $1 order by created_at desc limit 1", userUID).Scan(&cartUID, &isLocked); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, nil, nil
		}
		return nil, nil, err
	}
	return &cartUID, &isLocked, nil
}

func (r *Repository) CreateCart(ctx context.Context, tx *sqlx.Tx, userUID uuid.UUID) error {
	_, err := tx.ExecContext(ctx, queries.CreateCart, userUID)
	return err
}

func (r *Repository) LockCart(ctx context.Context, tx *sqlx.Tx, cartUID uuid.UUID) (bool, error) {
	res, err := tx.ExecContext(ctx, queries.LockCart, cartUID)
	if err != nil {
		return false, err
	}
	affected, err := res.RowsAffected()
	if err != nil {
		return false, err
	}
	return affected > 0, nil
}

func (r *Repository) Create(ctx context.Context, tx *sqlx.Tx, payload payloads.CreateOrderPayload) error {
	stmt, err := tx.PrepareNamedContext(ctx, queries.CreateOrder)
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.ExecContext(ctx, payload)
	return err
}
