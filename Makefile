.PHONY: help dev build seed test test-contracts lint format migrate clean

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Start all services in development mode
	docker compose up --build

build: ## Build all Docker images
	docker compose build

migrate: ## Run database migrations
	docker compose exec api alembic upgrade head

seed: ## Seed demo data (Chandigarh dataset)
	docker compose exec api python scripts/seed_demo_data.py

test: ## Run all backend tests
	docker compose exec api pytest services/api/tests -v

test-contracts: ## Run Solidity contract tests (requires Foundry)
	cd contracts && forge test -v

test-frontend: ## Run frontend tests
	cd apps/web && npm test

lint: ## Lint Python code
	docker compose exec api ruff check services/api/

format: ## Format Python code
	docker compose exec api ruff format services/api/

clean: ## Remove volumes and containers
	docker compose down -v --remove-orphans

logs: ## Tail all service logs
	docker compose logs -f

shell-api: ## Open a shell in the API container
	docker compose exec api bash

shell-db: ## Open a psql shell
	docker compose exec db psql -U localitylens localitylens

verify: ## Verify an evidence receipt (usage: make verify ID=<evidence-id>)
	docker compose exec api python scripts/verify_receipt.py $(ID)
