.PHONY: test backend-test frontend-build compose-config up

test: backend-test frontend-build

backend-test:
	cd backend && pytest

frontend-build:
	cd frontend && npm install && npm run build

compose-config:
	docker compose config

up:
	docker compose up --build
