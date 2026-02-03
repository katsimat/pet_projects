package middlewares

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"net/http"

	"github.com/google/uuid"

	"github.com/katsimat/backend/internal/utils/logger"
)

type traceIDKey struct{}

const TraceIDHeader = "X-Trace-ID"

func GetTraceID(ctx context.Context) string {
	if traceID, ok := ctx.Value(traceIDKey{}).(string); ok {
		return traceID
	}
	return ""
}

func TraceID(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		traceID := r.Header.Get(TraceIDHeader)
		if traceID == "" {
			bytes := make([]byte, 16)
			if _, err := rand.Read(bytes); err != nil {
				traceID = uuid.New().String()
			} else {
				traceID = hex.EncodeToString(bytes)
			}
		}

		ctx := context.WithValue(r.Context(), traceIDKey{}, traceID)
		ctx = context.WithValue(ctx, logger.TraceIDKey, traceID)
		r = r.WithContext(ctx)

		w.Header().Set(TraceIDHeader, traceID)

		next.ServeHTTP(w, r)
	})
}
