export_req:
	poetry export --without-hashes --format=requirements.txt > vanilla_pip/requirements.txt

dev_build:
	docker-compose -f docker-compose.dev.yml -p dev_django build -- web
	docker-compose -f docker-compose.dev.yml -p dev_django build

dev_run:
	docker-compose -f docker-compose.dev.yml -p dev_django up
	
dev_shell:
	docker-compose -f docker-compose.dev.yml -p dev_django run -v "$(shell pwd):/code" web bash

dev_down:
	docker-compose -f docker-compose.dev.yml -p dev_django down

dev_test:
	docker-compose -f docker-compose.dev.yml -p dev_django run web pytest


prod_build:
	docker-compose -f docker-compose.prod.yml -p prod_django build -- web

prod_run:
	docker-compose -f docker-compose.prod.yml -p prod_django up

prod_down:
	docker-compose -f docker-compose.prod.yml -p prod_django down