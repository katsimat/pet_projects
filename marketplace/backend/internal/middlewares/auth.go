package middlewares

import (
	"context"
	"net/http"
	"strings"

	"github.com/katsimat/backend/internal/configs"
	"github.com/katsimat/backend/internal/utils/auth"
)

type authClaimsKey struct{}

const AuthorizationHeader = "Authorization"

func GetAuthClaims(ctx context.Context) (auth.Claims, bool) {
	c, ok := ctx.Value(authClaimsKey{}).(auth.Claims)
	return c, ok
}

func Auth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		creds := configs.GetConfigManager().GetCredsConfig()
		secret := []byte(creds.Auth.Secret)
		if len(secret) == 0 {
			secret = []byte("dev_secret")
		}

		path := r.URL.Path

		if path == "/ping" || path == "/offers" || path == "/offers/get" || path == "/auth/login" {
			next.ServeHTTP(w, r)
			return
		}

		header := r.Header.Get(AuthorizationHeader)
		if header == "" {
			w.Header().Set("Content-Type", "application/json")
			http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
			return
		}
		parts := strings.SplitN(header, " ", 2)
		if len(parts) != 2 || strings.ToLower(parts[0]) != "bearer" {
			w.Header().Set("Content-Type", "application/json")
			http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
			return
		}

		claims, err := auth.Verify(secret, parts[1])
		if err != nil {
			w.Header().Set("Content-Type", "application/json")
			http.Error(w, `{"error":"unauthorized"}`, http.StatusUnauthorized)
			return
		}

		ctx := context.WithValue(r.Context(), authClaimsKey{}, claims)
		next.ServeHTTP(w, r.WithContext(ctx))
	})
}
