export_req:
	poetry export --without-hashes --format=requirements.txt > vanilla_pip/requirements.txt

project_id_dev ?= dev_django
dev_build:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} build -- web
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} build

dev_run:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} up
	
dev_shell:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} run -v "$(shell pwd):/code" web bash

dev_down:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} down

dev_test:
	docker-compose -f docker-compose.dev.yml -p ${project_id_dev} run web pytest

project_id_prod ?= prod_django
prod_build:
	docker-compose -f docker-compose.prod.yml -p ${project_id_prod} build -- web

prod_run:
	docker-compose -f docker-compose.prod.yml -p ${project_id_prod} up

prod_down:
	docker-compose -f docker-compose.prod.yml -p ${project_id_prod} down