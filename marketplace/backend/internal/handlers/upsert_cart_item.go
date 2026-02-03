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

type upsertCartItemUseCase interface {
	Handle(ctx context.Context, payload entities.UpsertCartItemPayload) (entities.UpsertCartItemResult, error)
}

type UpsertCartItemHandler struct {
	cartItemUseCase upsertCartItemUseCase
}

func NewUpsertCartItemHandler(cartItemUseCase upsertCartItemUseCase) *UpsertCartItemHandler {
	return &UpsertCartItemHandler{cartItemUseCase: cartItemUseCase}
}

func (h *UpsertCartItemHandler) Handle(ctx context.Context, req generated.UpsertCartItemRequest) (dto.Response, error) {
	claims, ok := middlewares.GetAuthClaims(ctx)
	if !ok {
		return nil, &dto.BadRequestError{Response: generated.UpsertCartItemResponse401{Error: "unauthorized"}, Message: "unauthorized"}
	}
	userUID, err := uuid.Parse(claims.UID)
	if err != nil {
		return nil, &dto.BadRequestError{Response: generated.UpsertCartItemResponse401{Error: "unauthorized"}, Message: "unauthorized"}
	}

	offerUID, err := uuid.Parse(req.OfferUid)
	if err != nil {
		msg := fmt.Sprintf("invalid offer_uid format: %s", req.OfferUid)
		return nil, &dto.BadRequestError{Response: generated.UpsertCartItemResponse400{Error: msg}, Message: msg}
	}

	_, err = h.cartItemUseCase.Handle(ctx, entities.UpsertCartItemPayload{
		UserUID:  userUID,
		OfferUID: offerUID,
		Quantity: req.Quantity,
	})
	if err != nil {
		if errors.Is(err, domain_errors.ErrCartNotFound) {
			msg := "cart not found"
			return nil, &dto.BadRequestError{Response: generated.UpsertCartItemResponse404{Error: msg}, Message: msg}
		}
		if errors.Is(err, domain_errors.ErrOfferNotFound) {
			msg := fmt.Sprintf("offer with uid %s not found", req.OfferUid)
			return nil, &dto.BadRequestError{Response: generated.UpsertCartItemResponse404{Error: msg}, Message: msg}
		}
		if errors.Is(err, domain_errors.ErrCartLocked) {
			msg := "cart is locked"
			return nil, &dto.BadRequestError{Response: generated.UpsertCartItemResponse409{Error: msg}, Message: msg}
		}
		return nil, fmt.Errorf("failed to upsert cart item: %w", err)
	}

	return dto.NoContentResponse{}, nil
}
