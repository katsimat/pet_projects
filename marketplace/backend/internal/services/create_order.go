package services

import (
	"context"
	"fmt"

	"github.com/google/uuid"
	"github.com/jmoiron/sqlx"

	"github.com/katsimat/backend/internal/entities"
	"github.com/katsimat/backend/internal/repositories/order/payloads"
)

type createOrderRepository interface {
	WithTx(ctx context.Context, fn func(tx *sqlx.Tx) error) error
	LockCart(ctx context.Context, tx *sqlx.Tx, cartUID uuid.UUID) (bool, error)
	Create(ctx context.Context, tx *sqlx.Tx, payload payloads.CreateOrderPayload) error
	GetLatestCartByUserUID(ctx context.Context, tx *sqlx.Tx, userUID uuid.UUID) (*uuid.UUID, *bool, error)
	CreateCart(ctx context.Context, tx *sqlx.Tx, userUID uuid.UUID) error
}

type CreateOrderService struct {
	orderRepo createOrderRepository
}

func NewCreateOrderService(orderRepo createOrderRepository) *CreateOrderService {
	return &CreateOrderService{orderRepo: orderRepo}
}

func (s *CreateOrderService) Handle(ctx context.Context, payload entities.CreateOrderPayload) (entities.CreateOrderResult, error) {
	res := entities.Order{
		UID:    uuid.New(),
		Status: entities.OrderStatusPending,
	}

	err := s.orderRepo.WithTx(ctx, func(tx *sqlx.Tx) error {
		cartUID, isLocked, err := s.orderRepo.GetLatestCartByUserUID(ctx, tx, payload.UserUID)
		if err != nil {
			return err
		}
		if cartUID == nil {
			return entities.ErrCartNotFound
		}
		if isLocked != nil && *isLocked {
			return entities.ErrCartLocked
		}

		ok, err := s.orderRepo.LockCart(ctx, tx, *cartUID)
		if err != nil {
			return err
		}
		if !ok {
			return entities.ErrCartLocked
		}

		if err := s.orderRepo.CreateCart(ctx, tx, payload.UserUID); err != nil {
			return fmt.Errorf("failed to create new cart: %w", err)
		}

		if err := s.orderRepo.Create(ctx, tx, payloads.CreateOrderPayload{
			UID:     res.UID,
			CartUID: *cartUID,
			Status:  res.Status,
		}); err != nil {
			return fmt.Errorf("failed to create order: %w", err)
		}

		return nil
	})
	if err != nil {
		return entities.Order{}, err
	}

	return res, nil
}
