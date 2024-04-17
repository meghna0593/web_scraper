# Web Scraper Assignment

## To start the Python virtual env:
    python -m venv venv
    source venv/bin/activate

## To install Django
    python -m pip install Django

## To run the server:
    python manage.py runserver    

## To create and run migrations:
    python manage.py makemigrations
    python manage.py migrate

## Endpoints

### Get All Products (paginated)
- **URL**: `/products`,  `/products/?page=2`, `/products/?page=3` ... 
- **Method**: GET
- **Description**: Retrieves a paginated list of all products available. Every page has atmost 10 products.
- **Example**: 
  ```http
  GET /products HTTP/1.1