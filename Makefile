.PHONY: build shell down clean format

build:
	docker compose build

shell:
	docker compose run app bash

clean:
	docker compose down --rmi local --remove-orphans

rebuild:
	make down
	make clean
	make build

format:
	docker compose run app uv run isort ./src
	docker compose run app uv run black ./src
	docker compose run app uv run mypy ./src
