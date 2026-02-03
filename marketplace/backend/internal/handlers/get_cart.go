package handlers

import (
	"context"
	"errors"

	"github.com/google/uuid"

	"github.com/katsimat/backend/generated"
	"github.com/katsimat/backend/internal/domain_errors"
	"github.com/katsimat/backend/internal/dto"
	"github.com/katsimat/backend/internal/entities"
	"github.com/katsimat/backend/internal/middlewares"
)

type getCartUseCase interface {
	Handle(ctx context.Context, payload entities.GetCartPayload) (entities.GetCartResult, error)
}

type GetCartHandler struct {
	uc getCartUseCase
}

func NewGetCartHandler(uc getCartUseCase) *GetCartHandler {
	return &GetCartHandler{uc: uc}
}

func (h *GetCartHandler) Handle(ctx context.Context, _ map[string]interface{}) (dto.Response, error) {
	claims, ok := middlewares.GetAuthClaims(ctx)
	if !ok {
		return nil, &dto.BadRequestError{Response: generated.GetCartResponse401{Error: "unauthorized"}, Message: "unauthorized"}
	}
	userUID, err := uuid.Parse(claims.UID)
	if err != nil {
		return nil, &dto.BadRequestError{Response: generated.GetCartResponse401{Error: "unauthorized"}, Message: "unauthorized"}
	}

	items, err := h.uc.Handle(ctx, entities.GetCartPayload{UserUID: userUID})
	if err != nil {
		if errors.Is(err, domain_errors.ErrCartNotFound) {
			return nil, &dto.BadRequestError{Response: generated.GetCartResponse404{Error: "cart not found"}, Message: "cart not found"}
		}
		if errors.Is(err, domain_errors.ErrCartLocked) {
			return nil, &dto.BadRequestError{Response: generated.GetCartResponse409{Error: "cart is locked"}, Message: "cart is locked"}
		}
		return nil, err
	}

	resItems := make([]generated.CartItem, 0, len(items))
	for _, it := range items {
		resItems = append(resItems, generated.CartItem{
			OfferUid: it.OfferUID.String(),
			Quantity: it.Quantity,
		})
	}

	return generated.GetCartResponse200{Items: resItems}, nil
}
