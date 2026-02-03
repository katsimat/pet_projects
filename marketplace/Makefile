.PHONY: build build-backend up up-db up-backend up-frontend down clean logs logs-backend logs-frontend db-clean migrate gen update

DC := docker-compose -f docker-compose.yml

build:
	$(DC) build

build-backend:
	$(DC) build backend

up:
	$(DC) up -d

up-db:
	$(DC) up -d postgres

up-backend:
	$(DC) up -d postgres backend

up-frontend:
	$(DC) up -d frontend

down:
	$(DC) down

clean:
	$(DC) down -v

logs:
	$(DC) logs -f

logs-backend:
	$(DC) logs -f backend

logs-frontend:
	$(DC) logs -f frontend

db-clean:
	@if $(DC) ps postgres | grep -q "Up"; then \
		$(DC) exec -T postgres psql -U marketplace -d marketplace -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" 2>/dev/null || true; \
	fi

# Usage: make migrate FILE=001_init.sql
migrate:
	@if [ -z "$(FILE)" ]; then \
		echo "Usage: make migrate FILE=001_init.sql"; \
		exit 1; \
	fi; \
	$(DC) exec -T postgres psql -U marketplace -d marketplace < backend/migrations/$(FILE)

gen:
	@$(MAKE) -C backend gen

update:
	@$(MAKE) -C backend update


