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
)

type getOfferUseCase interface {
	Handle(ctx context.Context, payload entities.GetOfferPayload) (entities.GetOfferResult, error)
}

type GetOfferHandler struct {
	offerUseCase getOfferUseCase
}

func NewGetOfferHandler(offerUseCase getOfferUseCase) *GetOfferHandler {
	return &GetOfferHandler{offerUseCase: offerUseCase}
}

func (h *GetOfferHandler) Handle(ctx context.Context, req generated.GetOfferParams) (dto.Response, error) {
	uid, err := uuid.Parse(req.Uid)
	if err != nil {
		msg := fmt.Sprintf("invalid uid format: %s", req.Uid)
		return nil, &dto.BadRequestError{
			Response: generated.GetOfferResponse400{Error: msg},
			Message:  msg,
		}
	}

	offer, err := h.offerUseCase.Handle(ctx, entities.GetOfferPayload{UID: uid})
	if err != nil {
		if errors.Is(err, domain_errors.ErrOfferNotFound) {
			msg := fmt.Sprintf("offer with uid %s not found", req.Uid)
			return nil, &dto.BadRequestError{
				Response: generated.GetOfferResponse404{Error: msg},
				Message:  msg,
			}
		}
		return nil, fmt.Errorf("failed to get offer: %w", err)
	}

	return generated.GetOfferResponse200{
		Uid: offer.UID.String(),
		Seller: generated.Seller{
			Email:   offer.SellerEmail,
			Name:    offer.SellerName,
			Surname: offer.SellerSurname,
		},
		Title:       offer.Title,
		Description: offer.Description,
		Price:       offer.Price,
		Quantity:    offer.Quantity,
		Status:      generated.OfferStatus(offer.Status),
	}, nil
}
