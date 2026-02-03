package use_cases

import (
	"context"

	"github.com/katsimat/backend/internal/entities"
)

type listOffersService interface {
	Handle(ctx context.Context, payload entities.ListOffersPayload) (entities.ListOffersResult, error)
}

type ListOffersUseCase struct {
	offerService listOffersService
}

func NewListOffersUseCase(offerService listOffersService) *ListOffersUseCase {
	return &ListOffersUseCase{offerService: offerService}
}

func (uc *ListOffersUseCase) Handle(ctx context.Context, payload entities.ListOffersPayload) (entities.ListOffersResult, error) {
	return uc.offerService.Handle(ctx, payload)
}
