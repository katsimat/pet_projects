package handlers

import (
	"context"

	"github.com/katsimat/backend/generated"
	"github.com/katsimat/backend/internal/dto"
)

func Ping(ctx context.Context, _ struct{}) (dto.Response, error) {
	return generated.PingResponse200{Status: "ok"}, nil
}
