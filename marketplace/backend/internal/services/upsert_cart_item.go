package services

import (
	"context"
	"fmt"

	"github.com/google/uuid"

	"github.com/katsimat/backend/internal/entities"
	cart_payloads "github.com/katsimat/backend/internal/repositories/cart/payloads"
)

type upsertCartItemRepository interface {
	UpsertItem(ctx context.Context, payload cart_payloads.UpsertCartItemPayload) error
	DeleteItem(ctx context.Context, cartUID uuid.UUID, offerUID uuid.UUID) (bool, error)
	GetLatestCartByUserUID(ctx context.Context, userUID uuid.UUID) (*uuid.UUID, *bool, error)
}

type upsertCartItemOfferRepository interface {
	GetByUID(ctx context.Context, uid uuid.UUID) (*entities.Offer, error)
}

type UpsertCartItemService struct {
	cartRepo  upsertCartItemRepository
	offerRepo upsertCartItemOfferRepository
}

func NewUpsertCartItemService(cartRepo upsertCartItemRepository, offerRepo upsertCartItemOfferRepository) *UpsertCartItemService {
	return &UpsertCartItemService{cartRepo: cartRepo, offerRepo: offerRepo}
}

func (s *UpsertCartItemService) Handle(ctx context.Context, payload entities.UpsertCartItemPayload) (entities.UpsertCartItemResult, error) {
	cartUID, isLocked, err := s.cartRepo.GetLatestCartByUserUID(ctx, payload.UserUID)
	if err != nil {
		return false, err
	}
	if cartUID == nil {
		return false, entities.ErrCartNotFound
	}
	if isLocked != nil && *isLocked {
		return false, entities.ErrCartLocked
	}

	offer, err := s.offerRepo.GetByUID(ctx, payload.OfferUID)
	if err != nil {
		return false, err
	}
	if offer == nil {
		return false, entities.ErrOfferNotFound
	}

	if payload.Quantity == 0 {
		_, err := s.cartRepo.DeleteItem(ctx, *cartUID, payload.OfferUID)
		if err != nil {
			return false, fmt.Errorf("failed to delete cart item: %w", err)
		}
		return true, nil
	}

	err = s.cartRepo.UpsertItem(ctx, cart_payloads.UpsertCartItemPayload{
		CartUID:  *cartUID,
		OfferUID: payload.OfferUID,
		Quantity: payload.Quantity,
	})
	if err != nil {
		return false, fmt.Errorf("failed to upsert cart item: %w", err)
	}

	return true, nil
}
