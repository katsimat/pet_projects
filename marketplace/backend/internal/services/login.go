package services

import (
	"context"

	"github.com/katsimat/backend/internal/entities"
)

type loginRepository interface {
	GetCredentialsByEmail(ctx context.Context, email string) (*entities.UserCredentials, error)
}

type LoginService struct {
	repo loginRepository
}

func NewLoginService(repo loginRepository) *LoginService {
	return &LoginService{repo: repo}
}

func (s *LoginService) Handle(ctx context.Context, payload entities.LoginPayload) (entities.LoginResult, error) {
	u, err := s.repo.GetCredentialsByEmail(ctx, payload.Email)
	if err != nil {
		return entities.LoginResult{}, err
	}
	if u == nil {
		return entities.LoginResult{}, entities.ErrUserNotFound
	}
	if u.Password != payload.Password {
		return entities.LoginResult{}, entities.ErrInvalidPassword
	}
	return entities.LoginResult{UID: u.UID.String(), Email: u.Email}, nil
}
