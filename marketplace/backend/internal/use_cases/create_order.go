package use_cases

import (
	"context"

	"github.com/katsimat/backend/internal/entities"
)

type createOrderService interface {
	Handle(ctx context.Context, payload entities.CreateOrderPayload) (entities.CreateOrderResult, error)
}

type CreateOrderUseCase struct {
	orderService createOrderService
}

func NewCreateOrderUseCase(orderService createOrderService) *CreateOrderUseCase {
	return &CreateOrderUseCase{orderService: orderService}
}

func (uc *CreateOrderUseCase) Handle(ctx context.Context, payload entities.CreateOrderPayload) (entities.CreateOrderResult, error) {
	return uc.orderService.Handle(ctx, payload)
}
