from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .swagger_definitions import manual_parameters, success_response

from .constants import PRODUCT_URLS
from .models import Product
from .serializers import ProductSerializer
from .utils import cache_product_data

class ProductPagination(PageNumberPagination):
    """
    Custom pagination class for products.
    """
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(APIView):
    """
    View for retrieving a paginated list of products.
    """
    pagination_class = ProductPagination

    @swagger_auto_schema(
        tags=['Products'],
        operation_summary="Get a list of products",
        operation_description="Retrieve a paginated list of products.",
        responses=success_response,
        manual_parameters=manual_parameters,
    )
    def get(self, request):
        """
        GET method for retrieving product list.

        Returns:
            Response: Response object containing product data
        """
        paginator = self.pagination_class()
        try:
            # Retrieve cached product data
            cached_products = self.get_cached_data()

            # Return bad request response if no products are cached or received
            if not cached_products:
                return Response("No products received", status=status.HTTP_400_BAD_REQUEST)
        
            products_data = []

            # Iterate over cached product data and extract relevant details
            for url in PRODUCT_URLS: # used URL as key in cache
                products_data.extend([
                    Product(
                        name=data["attributes"]["product.displayName"][0],
                        price=data["attributes"]["product.price"],
                        color=data.get("attributes",{}).get("product.sku.color.colorCode",[]),
                        url=data.get("attributes",{}).get("product.pdpURL",[""])[0],
                        image_urls=data.get("attributes",{}).get("product.sku.skuImages",[]), 
                        activity=data.get("attributes",{}).get("product.activity",[]),
                        title=data.get("attributes",{}).get("product.title",[""])[0],
                        category_hierarchy=data.get("attributes",{}).get("product.categoryHierarchy",[]),
                        default_sku=data["attributes"]["product.defaultSku"][0],
                        availability=data.get("attributes",{}).get("product.skuAvailabilityMap",[]),
                        currency_code=data.get("attributes",{}).get("currencyCode",[""])[0]
                    )
                    for data in cached_products[url]])

            # Paginate the product data
            products_paginated_data = paginator.paginate_queryset(products_data, request)
            serializer = ProductSerializer(products_paginated_data, many=True)
            
            # Return serialized product data if valid
            if serializer.is_valid:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else: # Return errors if invalid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except KeyError as e:
            error_message = f"KeyError: {str(e)}"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        except IndexError as e:
            error_message = f"IndexError: {str(e)}"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        

    def get_cached_data(self):
        """
        Helper method to retrieve cached product data.

        Returns:
            dict: Dictionary containing cached product data.
        """
        cached_data = cache.get_many(PRODUCT_URLS)
        if not cached_data:
            # Cache product data if not available
            cache_product_data(PRODUCT_URLS)
            cached_data = cache.get_many(PRODUCT_URLS)
        return cached_data if cached_data else None