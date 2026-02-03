package auth

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"errors"
	"strings"
	"time"
)

type Claims struct {
	Email string `json:"email"`
	UID   string `json:"uid"`
	Exp   int64  `json:"exp"`
}

var ErrInvalidToken = errors.New("invalid token")

var ErrTokenExpired = errors.New("token expired")

func Sign(secret []byte, c Claims) (string, error) {
	payloadBytes, err := json.Marshal(c)
	if err != nil {
		return "", err
	}
	payload := base64.RawURLEncoding.EncodeToString(payloadBytes)

	mac := hmac.New(sha256.New, secret)
	_, _ = mac.Write([]byte(payload))
	sig := base64.RawURLEncoding.EncodeToString(mac.Sum(nil))

	return payload + "." + sig, nil
}

func Verify(secret []byte, token string) (Claims, error) {
	parts := strings.Split(token, ".")
	if len(parts) != 2 {
		return Claims{}, ErrInvalidToken
	}
	payload := parts[0]
	sig := parts[1]

	mac := hmac.New(sha256.New, secret)
	_, _ = mac.Write([]byte(payload))
	expectedSig := base64.RawURLEncoding.EncodeToString(mac.Sum(nil))
	if !hmac.Equal([]byte(sig), []byte(expectedSig)) {
		return Claims{}, ErrInvalidToken
	}

	payloadBytes, err := base64.RawURLEncoding.DecodeString(payload)
	if err != nil {
		return Claims{}, ErrInvalidToken
	}
	var c Claims
	if err := json.Unmarshal(payloadBytes, &c); err != nil {
		return Claims{}, ErrInvalidToken
	}
	if c.Email == "" || c.UID == "" || c.Exp == 0 {
		return Claims{}, ErrInvalidToken
	}
	if time.Now().Unix() > c.Exp {
		return Claims{}, ErrTokenExpired
	}
	return c, nil
}
