package use_cases

import (
	"context"

	"github.com/katsimat/backend/internal/entities"
)

type getCartService interface {
	Handle(ctx context.Context, payload entities.GetCartPayload) (entities.GetCartResult, error)
}

type GetCartUseCase struct {
	svc getCartService
}

func NewGetCartUseCase(svc getCartService) *GetCartUseCase {
	return &GetCartUseCase{svc: svc}
}

func (uc *GetCartUseCase) Handle(ctx context.Context, payload entities.GetCartPayload) (entities.GetCartResult, error) {
	return uc.svc.Handle(ctx, payload)
}
