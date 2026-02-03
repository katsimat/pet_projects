package main

import (
	"context"
	"net/http"

	"github.com/katsimat/backend/internal/configs"
	"github.com/katsimat/backend/internal/handlers"
	"github.com/katsimat/backend/internal/middlewares"
	auth_repo "github.com/katsimat/backend/internal/repositories/auth"
	"github.com/katsimat/backend/internal/repositories/cart"
	"github.com/katsimat/backend/internal/repositories/offer"
	"github.com/katsimat/backend/internal/repositories/order"
	"github.com/katsimat/backend/internal/services"
	"github.com/katsimat/backend/internal/setup"
	"github.com/katsimat/backend/internal/use_cases"
	"github.com/katsimat/backend/internal/utils/logger"
)

var (
	middlewareChain = []middlewares.Middleware{
		middlewares.TraceIDMiddleware,
		middlewares.RequestLoggerMiddleware,
		middlewares.ResponseLoggerMiddleware,
		middlewares.AuthMiddleware,
	}
)

func main() {
	ctx := context.Background()

	db, err := setup.ConnectDatabase()
	if err != nil {
		logger.Errorf(ctx, "Failed to connect to database: %v", err)
		return
	}
	defer db.Close()
	logger.Info(ctx, "Database connected successfully")

	offerRepo := offer.NewRepository(db)
	cartRepo := cart.NewRepository(db)
	orderRepo := order.NewRepository(db)
	authRepo := auth_repo.NewRepository(db)

	listOffersService := services.NewListOffersService(offerRepo)
	listOffersUseCase := use_cases.NewListOffersUseCase(listOffersService)
	listOffersHandler := handlers.NewListOffersHandler(listOffersUseCase)

	getOfferService := services.NewGetOfferService(offerRepo)
	getOfferUseCase := use_cases.NewGetOfferUseCase(getOfferService)
	getOfferHandler := handlers.NewGetOfferHandler(getOfferUseCase)

	upsertCartItemService := services.NewUpsertCartItemService(cartRepo, offerRepo)
	upsertCartItemUseCase := use_cases.NewUpsertCartItemUseCase(upsertCartItemService)
	upsertCartItemHandler := handlers.NewUpsertCartItemHandler(upsertCartItemUseCase)

	getCartService := services.NewGetCartService(cartRepo)
	getCartUseCase := use_cases.NewGetCartUseCase(getCartService)
	getCartHandler := handlers.NewGetCartHandler(getCartUseCase)

	createOrderService := services.NewCreateOrderService(orderRepo)
	createOrderUseCase := use_cases.NewCreateOrderUseCase(createOrderService)
	createOrderHandler := handlers.NewCreateOrderHandler(createOrderUseCase)

	loginService := services.NewLoginService(authRepo)
	loginUseCase := use_cases.NewLoginUseCase(loginService)
	loginHandler := handlers.NewLoginHandler(loginUseCase)

	mux := http.NewServeMux()
	mux.HandleFunc("/ping", middlewares.HandleEndpoint(
		http.MethodGet,
		"/ping",
		handlers.Ping,
	))

	mux.HandleFunc("/auth/login", middlewares.HandleEndpoint(
		http.MethodPost,
		"/auth/login",
		loginHandler.Handle,
	))
	mux.HandleFunc("/offers", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			middlewares.HandleEndpoint(
				http.MethodGet,
				"/offers",
				listOffersHandler.Handle,
			)(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	mux.HandleFunc("/offers/get", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			middlewares.HandleEndpoint(
				http.MethodGet,
				"/offers/get",
				getOfferHandler.Handle,
			)(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	mux.HandleFunc("/cart_items", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodPost:
			middlewares.HandleEndpoint(
				http.MethodPost,
				"/cart_items",
				upsertCartItemHandler.Handle,
			)(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	mux.HandleFunc("/cart", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodGet:
			middlewares.HandleEndpoint(
				http.MethodGet,
				"/cart",
				getCartHandler.Handle,
			)(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	mux.HandleFunc("/orders", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodPost:
			middlewares.HandleEndpoint(
				http.MethodPost,
				"/orders",
				createOrderHandler.Handle,
			)(w, r)
		default:
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	handler := middlewares.Apply(mux, middlewareChain...)

	logger.Info(ctx, "Server starting on :8080")
	if err := http.ListenAndServe(":8080", handler); err != nil {
		logger.Errorf(ctx, "Server failed to start: %v", err)
	}

	configs.GetConfigManager().Stop()
}
