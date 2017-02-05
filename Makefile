db:
	dropdb --if-exists killington_local
	dropdb --if-exists killington_test
	dropuser --if-exists killington
	createuser -s killington
	createdb --owner=killington killington_local
	createdb --owner=killington killington_test

serve:
	honcho -f Procfile.dev start
