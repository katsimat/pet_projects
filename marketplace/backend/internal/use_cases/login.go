package use_cases

import (
	"context"

	"github.com/katsimat/backend/internal/entities"
)

type loginService interface {
	Handle(ctx context.Context, payload entities.LoginPayload) (entities.LoginResult, error)
}

type LoginUseCase struct {
	svc loginService
}

func NewLoginUseCase(svc loginService) *LoginUseCase {
	return &LoginUseCase{svc: svc}
}

func (uc *LoginUseCase) Handle(ctx context.Context, payload entities.LoginPayload) (entities.LoginResult, error) {
	return uc.svc.Handle(ctx, payload)
}
