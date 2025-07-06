run:
	python manage.py runserver

mig:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

test:
	python manage.py test
