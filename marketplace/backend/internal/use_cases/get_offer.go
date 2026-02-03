package use_cases

import (
	"context"

	"github.com/katsimat/backend/internal/entities"
)

type getOfferService interface {
	Handle(ctx context.Context, payload entities.GetOfferPayload) (entities.GetOfferResult, error)
}

type GetOfferUseCase struct {
	offerService getOfferService
}

func NewGetOfferUseCase(offerService getOfferService) *GetOfferUseCase {
	return &GetOfferUseCase{offerService: offerService}
}

func (uc *GetOfferUseCase) Handle(ctx context.Context, payload entities.GetOfferPayload) (entities.GetOfferResult, error) {
	return uc.offerService.Handle(ctx, payload)
}
