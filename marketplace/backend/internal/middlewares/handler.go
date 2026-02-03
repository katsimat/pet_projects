package middlewares

import (
	"context"
	"encoding/json"
	"io"
	"net/http"

	"github.com/katsimat/backend/internal/dto"
	"github.com/katsimat/backend/internal/utils/logger"
)

type HandlerFunc[Req any] func(ctx context.Context, req Req) (dto.Response, error)

func HandleEndpoint[Req any](method, path string, handler HandlerFunc[Req]) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()

		if r.Method != method {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		var req Req
		if r.Method == http.MethodGet || r.Method == http.MethodDelete {
			queryValues := r.URL.Query()
			reqMap := make(map[string]interface{})
			for key, values := range queryValues {
				if len(values) > 0 {
					reqMap[key] = values[0]
				}
			}
			reqBytes, err := json.Marshal(reqMap)
			if err != nil {
				logger.Errorf(ctx, "Failed to marshal query params: %v", err)
				http.Error(w, "Invalid query parameters", http.StatusBadRequest)
				return
			}
			if err := json.Unmarshal(reqBytes, &req); err != nil {
				logger.Errorf(ctx, "Failed to decode query params: %v", err)
				http.Error(w, "Invalid query parameters", http.StatusBadRequest)
				return
			}
		} else {
			if err := json.NewDecoder(r.Body).Decode(&req); err != nil && err != io.EOF {
				logger.Errorf(ctx, "Failed to decode request: %v", err)
				http.Error(w, "Invalid request body", http.StatusBadRequest)
				return
			}
		}

		resp, err := handler(ctx, req)
		if err != nil {
			if badReqErr, ok := err.(*dto.BadRequestError); ok {
				statusCode := badReqErr.Response.StatusCode()
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(statusCode)
				if err := json.NewEncoder(w).Encode(badReqErr.Response); err != nil {
					logger.Errorf(ctx, "Failed to encode response: %v", err)
					http.Error(w, "Failed to encode response", http.StatusInternalServerError)
					return
				}
				logger.Warnf(ctx, "Bad request: %s", badReqErr.Message)
				return
			}
			logger.Errorf(ctx, "Handler error: %v", err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		statusCode := resp.StatusCode()
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(statusCode)
		if statusCode == http.StatusNoContent {
			return
		}
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			logger.Errorf(ctx, "Failed to encode response: %v", err)
			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
			return
		}

		logger.Info(ctx, "Request processed successfully")
	}
}

type HandlerFuncWithQueryAndBody[QueryParams any, Body any] func(ctx context.Context, query QueryParams, body Body) (dto.Response, error)

func HandleEndpointWithQueryAndBody[QueryParams any, Body any](method, path string, handler HandlerFuncWithQueryAndBody[QueryParams, Body]) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		ctx := r.Context()

		if r.Method != method {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		queryValues := r.URL.Query()
		queryMap := make(map[string]any)
		for key, values := range queryValues {
			if len(values) > 0 {
				queryMap[key] = values[0]
			}
		}
		queryBytes, err := json.Marshal(queryMap)
		if err != nil {
			logger.Errorf(ctx, "Failed to marshal query params: %v", err)
			http.Error(w, "Invalid query parameters", http.StatusBadRequest)
			return
		}
		var queryParams QueryParams
		if err := json.Unmarshal(queryBytes, &queryParams); err != nil {
			logger.Errorf(ctx, "Failed to decode query params: %v", err)
			http.Error(w, "Invalid query parameters", http.StatusBadRequest)
			return
		}

		var body Body
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			logger.Errorf(ctx, "Failed to decode request: %v", err)
			http.Error(w, "Invalid request body", http.StatusBadRequest)
			return
		}

		resp, err := handler(ctx, queryParams, body)
		if err != nil {
			if badReqErr, ok := err.(*dto.BadRequestError); ok {
				statusCode := badReqErr.Response.StatusCode()
				w.Header().Set("Content-Type", "application/json")
				w.WriteHeader(statusCode)
				if err := json.NewEncoder(w).Encode(badReqErr.Response); err != nil {
					logger.Errorf(ctx, "Failed to encode response: %v", err)
					http.Error(w, "Failed to encode response", http.StatusInternalServerError)
					return
				}
				logger.Warnf(ctx, "Bad request: %s", badReqErr.Message)
				return
			}
			logger.Errorf(ctx, "Handler error: %v", err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		statusCode := resp.StatusCode()
		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(statusCode)
		if statusCode == http.StatusNoContent {
			return
		}
		if err := json.NewEncoder(w).Encode(resp); err != nil {
			logger.Errorf(ctx, "Failed to encode response: %v", err)
			http.Error(w, "Failed to encode response", http.StatusInternalServerError)
			return
		}

		logger.Info(ctx, "Request processed successfully")
	}
}
