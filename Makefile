.PHONY: setup up down logs test lint clean
setup:
	cp -n .env.example .env || true
up:
	docker compose up --build -d
down:
	docker compose down
logs:
	docker compose logs -f --tail=200
test:
	pytest -q
lint:
	ruff check app tests dashboard
clean:
	docker compose down -v --remove-orphans
