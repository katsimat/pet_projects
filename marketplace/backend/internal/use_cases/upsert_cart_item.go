package use_cases

import (
	"context"

	"github.com/katsimat/backend/internal/entities"
)

type upsertCartItemService interface {
	Handle(ctx context.Context, payload entities.UpsertCartItemPayload) (entities.UpsertCartItemResult, error)
}

type UpsertCartItemUseCase struct {
	cartItemService upsertCartItemService
}

func NewUpsertCartItemUseCase(cartItemService upsertCartItemService) *UpsertCartItemUseCase {
	return &UpsertCartItemUseCase{cartItemService: cartItemService}
}

func (uc *UpsertCartItemUseCase) Handle(ctx context.Context, payload entities.UpsertCartItemPayload) (entities.UpsertCartItemResult, error) {
	return uc.cartItemService.Handle(ctx, payload)
}
