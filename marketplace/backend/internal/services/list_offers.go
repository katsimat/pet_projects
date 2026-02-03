package services

import (
	"context"
	"fmt"

	"github.com/katsimat/backend/internal/entities"
)

type listOffersRepository interface {
	ListActiveBySearch(ctx context.Context, q string) ([]entities.Offer, error)
}

type ListOffersService struct {
	offerRepo listOffersRepository
}

func NewListOffersService(offerRepo listOffersRepository) *ListOffersService {
	return &ListOffersService{offerRepo: offerRepo}
}

func (s *ListOffersService) Handle(ctx context.Context, payload entities.ListOffersPayload) (entities.ListOffersResult, error) {
	offers, err := s.offerRepo.ListActiveBySearch(ctx, payload.Query)
	if err != nil {
		return nil, fmt.Errorf("failed to list offers: %w", err)
	}
	return offers, nil
}
