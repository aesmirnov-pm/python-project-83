dev:
	poetry run flask --app page_analyzer:app run

install:
	poetry install

lint:
	poetry run flake8 page_analyzer

start:
	poetry run gunicorn -w 5 page_analyzer:app