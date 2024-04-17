from drf_yasg import openapi
from .serializers import ProductSerializer


manual_parameters=[
        openapi.Parameter(
            'page',
            openapi.IN_QUERY,
            description="Page number",
            type=openapi.TYPE_INTEGER
        )
    ]

product_item_example = {
    "name": openapi.Schema(type=openapi.TYPE_STRING, description="Product name"),
    "price": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER), description="Product Prices"),
    "color": openapi.Schema(type=openapi.TYPE_STRING, description="Product colors"),
    "url": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI, description="Product URL"),
    "image_urls": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI), description="List of image URLs"),
    "activity": openapi.Schema(type=openapi.TYPE_STRING, description="Product can be used with activity"),
    "title": openapi.Schema(type=openapi.TYPE_STRING, description="Product title"),
    "category_hierarchy": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="Category hierarchy"),
    "default_sku": openapi.Schema(type=openapi.TYPE_STRING, description="Default SKU"),
    "availability": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING), description="Product availability"),
    "currency_code": openapi.Schema(type=openapi.TYPE_STRING, description="Currency code"),
}

product_list_example = [product_item_example, product_item_example]  # List of product items

success_response = {
    "200": openapi.Response(
        description="Successful response",
        schema=ProductSerializer(many=True),
        examples={'application/json': product_list_example}, 
    ),
}
