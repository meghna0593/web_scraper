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


## AWS Lambda / API Gateway instructions
Because of resource constraints, utilizing an AWS Lambda function was not feasible.  
However, the implementation is pretty straight-forward.

1. Lambda Function Setup:
- Write a lambda function to extract product details
def extract_product_details(event, context):
    # Extract URLs from the event
    urls = event.get('urls', [])
    
    product_details = []
    
    # Iterate over URLs and extract product details
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            # Extract product details and append to product_details list
            product_details.append({
                'name': response[..]['product.displayName'],
                # Add more product details here
            })
    
    # Return product details as JSON
    return {
        'statusCode': 200,
        'body': json.dumps(product_details)
    }

2. API Gateway Configuration:
- Create a new REST API in the AWS API Gateway console.
- Define a resource (e.g., /products) and create a GET method for it.
- In the Integration Request configuration, set up the integration type as "Lambda Function" and select the Lambda function created above.
- Configure any required request parameters (e.g., urls) and map them to the input format expected by the Lambda function.
- Define the Response Model to specify the structure of the response returned by the Lambda function.
- Test the Lambda function in the AWS Lambda console by providing sample input data.
- Test the API endpoint using tools like cURL or Postman, passing a list of URLs as query parameters.