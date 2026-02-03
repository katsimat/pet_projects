package middlewares

import (
	"bytes"
	"net/http"

	"github.com/katsimat/backend/internal/utils/logger"
)

type responseWriter struct {
	http.ResponseWriter
	statusCode int
	body       *bytes.Buffer
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

func (rw *responseWriter) Write(b []byte) (int, error) {
	if rw.body == nil {
		rw.body = &bytes.Buffer{}
	}
	rw.body.Write(b)
	return rw.ResponseWriter.Write(b)
}

func ResponseLogger(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		rw := &responseWriter{
			ResponseWriter: w,
			statusCode:     http.StatusOK,
		}

		next.ServeHTTP(rw, r)

		ctx := r.Context()

		switch {
		case rw.statusCode >= 500:
			logger.Errorf(ctx, "Response %d %s", rw.statusCode, http.StatusText(rw.statusCode))
		case rw.statusCode >= 400:
			logger.Warnf(ctx, "Response %d %s", rw.statusCode, http.StatusText(rw.statusCode))
		case rw.statusCode >= 300:
			logger.Infof(ctx, "Response %d %s", rw.statusCode, http.StatusText(rw.statusCode))
		default:
			logger.Infof(ctx, "Response %d %s", rw.statusCode, http.StatusText(rw.statusCode))
		}

		if rw.body != nil && rw.body.Len() > 0 {
			logger.Infof(ctx, "response body: %s", rw.body.String())
		}
	})
}
