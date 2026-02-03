.PHONY: build run stop clean db-clean migrate test run-local logs db-connect setup-creds gen update

# Build the application
build:
	@echo "Use root Makefile: make build"

# Run the application
run:
	@echo "Use root Makefile: make up-backend"

# Stop the application
stop:
	@echo "Use root Makefile: make down"

# Generate code from OpenAPI specification
# Supports multiple YAML files in api/ directory
# All types are generated into a single types.go file
# Also creates default config files if they don't exist
gen:
	@echo "Generating code from OpenAPI specification..."
	@mkdir -p generated
	@rm -f generated/types.go
	@touch generated/types.go
	@echo "package generated" > generated/types.go
	@echo "" >> generated/types.go
	@echo "// Code generated from OpenAPI specifications. DO NOT EDIT." >> generated/types.go
	@for yaml_file in api/*.yaml api/*.yml; do \
		if [ -f "$$yaml_file" ]; then \
			echo "Processing $$yaml_file..."; \
			temp_file=$$(mktemp); \
			go run github.com/deepmap/oapi-codegen/cmd/oapi-codegen@latest -generate types -package generated -o $$temp_file $$yaml_file 2>/dev/null || continue; \
			sed -n '/^\/\/ /p; /^type /,/^}/p; /^const /,/^)/p' $$temp_file | grep -v "^package " | grep -v "^import " | grep -v "^\/\/ Package" >> generated/types.go || true; \
			rm -f $$temp_file; \
		fi; \
	done
	@echo "Adding StatusCode() methods to response types..."
	@go build -o /tmp/add_status_methods ./scripts/add_status_methods.go
	@/tmp/add_status_methods generated/types.go
	@rm -f /tmp/add_status_methods
	@go fmt generated/types.go
	@echo "Code generated in generated/types.go"
	@echo "Checking config files..."
	@if [ ! -f configs/logging.json ]; then \
		echo "Creating configs/logging.json from example..."; \
		cp configs/example/logging.json.example configs/logging.json; \
		echo "⚠️  Please edit configs/logging.json with your settings"; \
	fi
	@if [ ! -f configs/database.json ]; then \
		echo "Creating configs/database.json from example..."; \
		cp configs/example/database.json.example configs/database.json; \
		echo "⚠️  Please edit configs/database.json with your settings"; \
	fi
	@if [ ! -f configs/creds.json ]; then \
		echo "Creating configs/creds.json from example..."; \
		cp configs/example/creds.json.example configs/creds.json; \
		echo "⚠️  Please edit configs/creds.json with your credentials"; \
	fi

# Update: remove generated files and regenerate
update:
	@echo "Removing generated files..."
	@rm -rf generated
	@echo "Regenerating code..."
	@$(MAKE) gen

# Clean up generated files and containers/volumes
clean:
	@echo "Use root Makefile: make clean"

# Clean up database only
db-clean:
	@echo "Use root Makefile: make db-clean"

# Run migrations
# Usage: make migrate FILE=001_init.sql
migrate:
	@echo "Use root Makefile: make migrate FILE=001_init.sql"

# Run tests
test:
	go test ./...

# Run the application locally (without docker)
run-local:
	go run cmd/main.go

# Show logs
logs:
	@echo "Use root Makefile: make logs"

# Setup credentials file from example
# Usage: make setup-creds
setup-creds:
	@if [ -f configs/creds.json ]; then \
		echo "Warning: configs/creds.json already exists. Skipping."; \
	else \
		cp configs/example/creds.json.example configs/creds.json; \
		echo "Created configs/creds.json from example. Please edit it with your credentials."; \
	fi

# Connect to PostgreSQL database
# Reads credentials from configs/creds.json and database settings from configs/database.json
db-connect:
	@if [ ! -f configs/creds.json ]; then \
		echo "Error: configs/creds.json not found. Please create it with database credentials."; \
		exit 1; \
	fi; \
	if [ ! -f configs/database.json ]; then \
		echo "Error: configs/database.json not found. Please create it with database settings."; \
		exit 1; \
	fi; \
	user=$$(grep -o '"user": "[^"]*"' configs/creds.json | cut -d'"' -f4); \
	password=$$(grep -o '"password": "[^"]*"' configs/creds.json | cut -d'"' -f4); \
	host=$$(grep -o '"host": "[^"]*"' configs/database.json | cut -d'"' -f4); \
	port=$$(grep -o '"port": [0-9]*' configs/database.json | grep -o '[0-9]*'); \
	dbname=$$(grep -o '"dbname": "[^"]*"' configs/database.json | cut -d'"' -f4); \
	PGPASSWORD=$$password psql -h $$host -p $$port -U $$user -d $$dbname
