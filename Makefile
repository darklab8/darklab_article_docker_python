init:
	poetry install

dev:
	poetry run -- mkdocs serve

remote:
	git remote set-url origin git@github.com-dd84ai:darklab8/darklab_article_docker_python.git
	git remote set-url --add --push origin git@github.com-dd84ai:darklab8/darklab_article_docker_python.git
	git remote set-url --add --push origin git@gitlab.com-dd84ai:darklab2/darklab_article_docker_python.git