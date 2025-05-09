dev-install:
	pip install -r src/requirements.txt
	pip install -r src/requirements-dev.txt

fmt:
	isort .
	black .

lint:
	flake8 .
	mypy .

tag:
	make lint
	make test
	git fetch --tags
	git for-each-ref --sort=-creatordate --format '%(refname:short)' refs/tags | head -n 1
	@read -p "Enter tag name: " tag_name; \
	git tag -a "$$tag_name" -m "$$tag_name" && git push origin "$$tag_name"

lint-annotate:
	flake8 .
	mypy --disallow-untyped-defs .

superuser:
	python src/manage.py createsuperuser

runserver:
	python src/manage.py runserver

static:
	python src/manage.py collectstatic

makemigrations:
	python src/manage.py makemigrations

migrate:
	python src/manage.py migrate

shell:
	python src/manage.py shell

test:
	pytest --cov=src src/_tests --blockage --cov-report term-missing
