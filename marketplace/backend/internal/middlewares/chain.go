package middlewares

import "net/http"

type Middleware func(http.Handler) http.Handler

var (
	TraceIDMiddleware        = Middleware(TraceID)
	AuthMiddleware           = Middleware(Auth)
	RequestLoggerMiddleware  = Middleware(RequestLogger)
	ResponseLoggerMiddleware = Middleware(ResponseLogger)
)

func Apply(handler http.Handler, middlewares ...Middleware) http.Handler {
	for i := len(middlewares) - 1; i >= 0; i-- {
		handler = middlewares[i](handler)
	}
	return handler
}
