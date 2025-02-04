build:
	docker compose -f docker-compose.local.yml build

dev:
	docker compose -f docker-compose.local.yml up -d

flake8:
	docker compose -f docker-compose.local.yml run --rm app flake8 .

pylint:
	docker compose -f docker-compose.local.yml run --rm app pylint app.py
	docker compose -f docker-compose.local.yml run --rm app pylint src/**

down:
	docker compose -f docker-compose.local.yml down

stop:
	docker compose -f docker-compose.local.yml stop

restart:
	docker compose -f docker-compose.local.yml restart
