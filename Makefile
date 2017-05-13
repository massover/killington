dropdb:
	dropdb --if-exists killington_local
	dropdb --if-exists killington_test
	dropuser --if-exists killington

createdb:
	createuser -s killington
	createdb --owner=killington killington_local
	createdb --owner=killington killington_test

migrate:
	python manage.py migrate


db: dropdb createdb migrate seeds

seeds:
	python manage.py seed users shows

serve:
	honcho -f Procfile.dev start

test:
	py.test -v --durations=25

lint:
	flake8