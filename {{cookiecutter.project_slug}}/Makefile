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

db.migrate:
	if [ ! -d "src/migrations" ]; then \
		docker compose -f docker-compose.local.yml run --rm app flask --app run.py db init; \
	fi
	make db.auto_discover_models
	docker compose -f docker-compose.local.yml run --rm app flask --app run.py db migrate
	make db.migrate.upgrade

db.migrate.upgrade:
	docker compose -f docker-compose.local.yml run --rm app flask --app run.py db upgrade

db.seed:
	docker compose -f docker-compose.local.yml run --rm app flask --app run.py seed run

db.auto_discover_models:
	docker compose -f docker-compose.local.yml run --rm app flask --app run.py database auto_discover

module.create:
	docker compose -f docker-compose.local.yml run --rm app flask --app run.py module generate --name $(module)
	#"Example: make module.create module=MyModule"
