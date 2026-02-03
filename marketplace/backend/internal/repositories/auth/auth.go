package auth

import (
	"context"
	"database/sql"
	"errors"

	"github.com/jmoiron/sqlx"

	"github.com/katsimat/backend/internal/entities"
)

type Repository struct {
	db *sqlx.DB
}

func NewRepository(db *sqlx.DB) *Repository {
	return &Repository{db: db}
}

func (r *Repository) GetCredentialsByEmail(ctx context.Context, email string) (*entities.UserCredentials, error) {
	var u entities.UserCredentials
	if err := r.db.GetContext(ctx, &u, "select uid, email, password from users where email = $1", email); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, nil
		}
		return nil, err
	}
	return &u, nil
}
