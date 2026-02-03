package middlewares

import (
	"bytes"
	"io"
	"net/http"
	"time"

	"github.com/katsimat/backend/internal/utils/logger"
)

func RequestLogger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		ctx := r.Context()

		var bodyBytes []byte
		if r.Body != nil {
			bodyBytes, _ = io.ReadAll(r.Body)
			r.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))
		}

		logger.Infof(ctx, "new incoming request %s %s from %s", r.Method, r.URL.Path, r.RemoteAddr)
		if len(bodyBytes) > 0 {
			logger.Infof(ctx, "request body: %s", string(bodyBytes))
		}

		next.ServeHTTP(w, r)

		duration := time.Since(start)
		logger.Infof(ctx, "request finished for %s %s in %v", r.Method, r.URL.Path, duration)
	})
}
