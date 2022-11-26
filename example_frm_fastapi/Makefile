makemigration:
	alembic -c src/alembic.ini revision --autogenerate -m "$1"

migrate:
	alembic -c src/alembic.ini upgrade head

export_req:
	poetry export --without-hashes --format=requirements.txt > vanilla_pip/requirements.txt

project_id_dev ?= dev_fastapi
dev_build:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} build -- web
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} build

dev_run:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} up
	
dev_shell:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} run -v "$(shell pwd):/code" web bash

dev_shell2:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} run web bash

dev_down:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} down

dev_test:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} run web pytest

project_id_prod ?= prod_fastapi
prod_build:
	docker-compose -f docker-compose.prod.yml -p project_id_prod build -- web
	docker-compose -f docker-compose.prod.yml -p project_id_prod build

prod_run:
	docker-compose -f docker-compose.prod.yml -p project_id_prod up

prod_down:
	docker-compose -f docker-compose.prod.yml -p project_id_prod down