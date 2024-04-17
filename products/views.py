from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
import requests

from .constants import PRODUCT_URLS
from .models import Product
from .serializers import ProductSerializer

class ProductPagination(PageNumberPagination):
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductListView(APIView):
    pagination_class = ProductPagination
    def get(self, request):
        paginator = self.pagination_class()
        try:
            products_data = []

            for url in PRODUCT_URLS: # used url as key in cache
                response = requests.get(url)
                if response.status_code == 200:
                    products = (response.json())["contents"][0]["mainContent"][0]["contents"][0]["records"]
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
                    for data in products])

            products_paginated_data = paginator.paginate_queryset(products_data, request)
            serializer = ProductSerializer(products_paginated_data, many=True)
            
            if serializer.is_valid:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            error_message = f"KeyError: {str(e)}"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        except IndexError as e:
            error_message = f"IndexError: {str(e)}"
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
