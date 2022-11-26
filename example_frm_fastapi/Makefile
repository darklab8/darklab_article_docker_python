makemigration:
	alembic -c src/alembic.ini revision --autogenerate -m "$1"

migrate:
	alembic -c src/alembic.ini upgrade head

export_req:
	poetry export --without-hashes --format=requirements.txt > vanilla_pip/requirements.txt


dev_build:
	docker-compose -f docker-compose.dev.yml -p dev_fastapi build -- web
	docker-compose -f docker-compose.dev.yml -p dev_fastapi build

dev_run:
	docker-compose -f docker-compose.dev.yml -p dev_fastapi up
	
dev_shell:
	docker-compose -f docker-compose.dev.yml -p dev_fastapi run -v "$(shell pwd):/code" web bash

dev_shell2:
	docker-compose -f docker-compose.dev.yml -p dev_fastapi run web bash

dev_down:
	docker-compose -f docker-compose.dev.yml -p dev_fastapi down

dev_test:
	docker-compose -f docker-compose.dev.yml -p dev_fastapi run web pytest

prod_build:
	docker-compose -f docker-compose.prod.yml -p prod_fastapi build -- web
	docker-compose -f docker-compose.prod.yml -p prod_fastapi build

prod_run:
	docker-compose -f docker-compose.prod.yml -p prod_fastapi up

prod_down:
	docker-compose -f docker-compose.prod.yml -p prod_fastapi down