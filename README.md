# Web Scraper Assignment

This Django application is responsible for scraping product details from provided URLs. 

The relevant product details being pulled are:
- Product SKU
- Product Name
- Product Title
- Product Price
- Product Availability
- Product Image URLs
- Product Catergory Hierarchy
- Product Activity
- Product Colors
- Product Detail Page URL
- Currency Code

## To start the Python virtual env:
    python -m venv venv
    source venv/bin/activate

## To install Django
    make install

## To run the server:
    make runserver   

## To run tests:
    make test

## To create and run migrations:
    make migrate

## To undo migrations:
    make undo_migrate <app_name> <migration_number_to_retain>


## Endpoints

### Get All Products (paginated)
- **URL**: `/products`,  `/products/?page=2`, `/products/?page=3` ... 
- **Method**: GET
- **Description**: Retrieves a paginated list of all products available. Every page has atmost 10 products.
- **Example**: 
  ```http
  GET /products HTTP/1.1


### Swagger docs
- **URL**: `/swagger`
- **Method**: GET
- **Description**: Details on /products endpoint. Also, retrieves a paginated list of all products available. 
- **Parameters**: Add page numbers in the section available


### Redocs
- **URL**: `/redoc`
- **Description**: Details on /products endpoint