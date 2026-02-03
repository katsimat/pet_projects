package handlers

import (
	"context"
	"fmt"

	"github.com/katsimat/backend/generated"
	"github.com/katsimat/backend/internal/dto"
	"github.com/katsimat/backend/internal/entities"
)

type listOffersUseCase interface {
	Handle(ctx context.Context, payload entities.ListOffersPayload) (entities.ListOffersResult, error)
}

type ListOffersHandler struct {
	offerUseCase listOffersUseCase
}

func NewListOffersHandler(offerUseCase listOffersUseCase) *ListOffersHandler {
	return &ListOffersHandler{offerUseCase: offerUseCase}
}

func (h *ListOffersHandler) Handle(ctx context.Context, req generated.ListOffersParams) (dto.Response, error) {
	q := ""
	if req.TextSearch != nil {
		q = *req.TextSearch
	}

	offers, err := h.offerUseCase.Handle(ctx, entities.ListOffersPayload{Query: q})
	if err != nil {
		return nil, fmt.Errorf("failed to list offers: %w", err)
	}

	res := make([]generated.Offer, 0, len(offers))
	for _, o := range offers {
		res = append(res, generated.Offer{
			Uid: o.UID.String(),
			Seller: generated.Seller{
				Email:   o.SellerEmail,
				Name:    o.SellerName,
				Surname: o.SellerSurname,
			},
			Title:       o.Title,
			Description: o.Description,
			Price:       o.Price,
			Quantity:    o.Quantity,
			Status:      generated.OfferStatus(o.Status),
		})
	}

	return generated.ListOffersResponse200{Offers: res}, nil
}
