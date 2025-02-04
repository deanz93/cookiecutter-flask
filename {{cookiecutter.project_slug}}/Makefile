build:
	docker compose -f docker-compose.local.yml build

dev:
	docker compose -f docker-compose.local.yml up -d

flake8:
	docker compose -f docker-compose.local.yml run --rm app flake8 .

pylint:
	docker compose -f docker-compose.local.yml run --rm app pylint run.py
	docker compose -f docker-compose.local.yml run --rm app pylint src/**

down:
	docker compose -f docker-compose.local.yml down

stop:
	docker compose -f docker-compose.local.yml stop

restart:
	docker compose -f docker-compose.local.yml restart

migrate:
	docker compose -f docker-compose.local.yml run --rm app flask --app run.py db migrate
	make migrate.upgrade

migrate.upgrade:
	docker compose -f docker-compose.local.yml run --rm app flask --app run.py db upgrade