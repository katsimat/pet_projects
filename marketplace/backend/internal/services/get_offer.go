package services

import (
	"context"

	"github.com/google/uuid"

	"github.com/katsimat/backend/internal/entities"
)

type getOfferRepository interface {
	GetByUID(ctx context.Context, uid uuid.UUID) (*entities.Offer, error)
}

type GetOfferService struct {
	offerRepo getOfferRepository
}

func NewGetOfferService(offerRepo getOfferRepository) *GetOfferService {
	return &GetOfferService{offerRepo: offerRepo}
}

func (s *GetOfferService) Handle(ctx context.Context, payload entities.GetOfferPayload) (entities.GetOfferResult, error) {
	offer, err := s.offerRepo.GetByUID(ctx, payload.UID)
	if err != nil {
		return entities.Offer{}, err
	}
	if offer == nil {
		return entities.Offer{}, entities.ErrOfferNotFound
	}
	return *offer, nil
}
