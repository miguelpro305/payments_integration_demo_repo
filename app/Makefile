.PHONY: up down restart logs reset-db

up:
	docker compose -f docker-compose.yml up -d --build

down:
	docker compose -f docker-compose.yml down

restart: down up

logs:
	docker compose -f docker-compose.yml logs -f

reset-db:
	docker compose -f docker-compose.yml down -v
	docker volume rm postgres_data || true
	docker compose -f docker-compose.yml up -d --build
