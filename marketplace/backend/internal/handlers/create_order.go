package handlers

import (
	"context"
	"errors"
	"fmt"

	"github.com/google/uuid"

	"github.com/katsimat/backend/generated"
	"github.com/katsimat/backend/internal/domain_errors"
	"github.com/katsimat/backend/internal/dto"
	"github.com/katsimat/backend/internal/entities"
	"github.com/katsimat/backend/internal/middlewares"
)

type createOrderUseCase interface {
	Handle(ctx context.Context, payload entities.CreateOrderPayload) (entities.CreateOrderResult, error)
}

type CreateOrderHandler struct {
	orderUseCase createOrderUseCase
}

func NewCreateOrderHandler(orderUseCase createOrderUseCase) *CreateOrderHandler {
	return &CreateOrderHandler{orderUseCase: orderUseCase}
}

func (h *CreateOrderHandler) Handle(ctx context.Context, req generated.CreateOrderRequest) (dto.Response, error) {
	claims, ok := middlewares.GetAuthClaims(ctx)
	if !ok {
		return nil, &dto.BadRequestError{Response: generated.CreateOrderResponse401{Error: "unauthorized"}, Message: "unauthorized"}
	}
	userUID, err := uuid.Parse(claims.UID)
	if err != nil {
		return nil, &dto.BadRequestError{Response: generated.CreateOrderResponse401{Error: "unauthorized"}, Message: "unauthorized"}
	}

	order, err := h.orderUseCase.Handle(ctx, entities.CreateOrderPayload{UserUID: userUID})
	if err != nil {
		if errors.Is(err, domain_errors.ErrCartNotFound) {
			msg := "cart not found"
			return nil, &dto.BadRequestError{Response: generated.CreateOrderResponse404{Error: msg}, Message: msg}
		}
		if errors.Is(err, domain_errors.ErrCartLocked) {
			msg := "cart is locked"
			return nil, &dto.BadRequestError{Response: generated.CreateOrderResponse409{Error: msg}, Message: msg}
		}
		return nil, fmt.Errorf("failed to create order: %w", err)
	}

	return generated.CreateOrderResponse201{
		Uid:    order.UID.String(),
		Status: generated.OrderStatus(order.Status),
	}, nil
}
