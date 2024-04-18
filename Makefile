# Install Django
install:
	pip install -r requirements.txt
	
# Run the server
runserver:
	python manage.py runserver

# Run tests
test:
	python manage.py test

# Create and run migrations
migrate:
	python manage.py makemigrations
	python manage.py migrate

# Undo migrations for a specific app and migration number
undo_migrate:
	python manage.py migrate $(app) $(migration_number_to_retain)
