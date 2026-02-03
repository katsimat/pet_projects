package entities

type ListOffersPayload struct {
	Query string
}

type ListOffersResult = []Offer
