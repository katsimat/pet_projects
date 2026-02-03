package services

import (
	"context"

	"github.com/google/uuid"

	"github.com/katsimat/backend/internal/entities"
)

type getCartRepository interface {
	GetLatestCartByUserUID(ctx context.Context, userUID uuid.UUID) (*uuid.UUID, *bool, error)
	ListItems(ctx context.Context, cartUID uuid.UUID) ([]entities.CartItem, error)
}

type GetCartService struct {
	repo getCartRepository
}

func NewGetCartService(repo getCartRepository) *GetCartService {
	return &GetCartService{repo: repo}
}

func (s *GetCartService) Handle(ctx context.Context, payload entities.GetCartPayload) (entities.GetCartResult, error) {
	cartUID, isLocked, err := s.repo.GetLatestCartByUserUID(ctx, payload.UserUID)
	if err != nil {
		return nil, err
	}
	if cartUID == nil {
		return nil, entities.ErrCartNotFound
	}
	if isLocked != nil && *isLocked {
		return nil, entities.ErrCartLocked
	}

	items, err := s.repo.ListItems(ctx, *cartUID)
	if err != nil {
		return nil, err
	}
	return items, nil
}
