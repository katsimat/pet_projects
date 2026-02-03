package handlers

import (
	"context"
	"errors"
	"time"

	"github.com/katsimat/backend/generated"
	"github.com/katsimat/backend/internal/configs"
	"github.com/katsimat/backend/internal/domain_errors"
	"github.com/katsimat/backend/internal/dto"
	"github.com/katsimat/backend/internal/entities"
	"github.com/katsimat/backend/internal/utils/auth"
)

type loginUseCase interface {
	Handle(ctx context.Context, payload entities.LoginPayload) (entities.LoginResult, error)
}

type LoginHandler struct {
	uc loginUseCase
}

func NewLoginHandler(uc loginUseCase) *LoginHandler {
	return &LoginHandler{uc: uc}
}

func (h *LoginHandler) Handle(ctx context.Context, req generated.LoginRequest) (dto.Response, error) {
	res, err := h.uc.Handle(ctx, entities.LoginPayload{Email: req.Email, Password: req.Password})
	if err != nil {
		if errors.Is(err, domain_errors.ErrUserNotFound) || errors.Is(err, domain_errors.ErrInvalidPassword) {
			return nil, &dto.BadRequestError{
				Response: generated.LoginResponse401{Error: "invalid credentials"},
				Message:  "invalid credentials",
			}
		}
		return nil, err
	}

	creds := configs.GetConfigManager().GetCredsConfig()
	secret := []byte(creds.Auth.Secret)
	if len(secret) == 0 {
		secret = []byte("dev_secret")
	}

	token, err := auth.Sign(secret, auth.Claims{
		Email: res.Email,
		UID:   res.UID,
		Exp:   time.Now().Add(time.Hour).Unix(),
	})
	if err != nil {
		return nil, err
	}

	return generated.LoginResponse200{Token: token}, nil
}
