from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from unittest.mock import patch, MagicMock
from .utils import cache_product_data
from .views import ProductListView

class ProductListViewTest(APITestCase):

    def setUp(self):
        # Setting up API request factory and URL for the view
        self.factory = APIRequestFactory()
        self.view = ProductListView.as_view()
        self.url = reverse("product_list")
        
    # Test for successful retrieval of products
    @patch('products.views.ProductListView.get_cached_data')
    def test_get_products_success(self,mock_get_cached_data):
        # Mock cached product data
        mock_cached_data = {
            'https://example.com/products': [
                {
                    'attributes': {
                        'product.displayName': ['Product 1'],
                        'product.price': [10.0],
                        'product.sku.color.colorCode': ['Red'],
                        'product.pdpURL': ['https://example.com/product/1'],
                        'product.sku.skuImages': ['https://example.com/image1.jpg'],
                        'product.activity': ['Activity 1'],
                        'product.title': ['Title 1'],
                        'product.categoryHierarchy': ['Category 1'],
                        'product.defaultSku': ['SKU123'],
                        'product.skuAvailabilityMap': ['In Stock'],
                        'currencyCode': ['USD']
                    }
                },
                {
                    'attributes': {
                        'product.displayName': ['Product 2'],
                        'product.price': [20.0],
                        'product.sku.color.colorCode': ['Blue'],
                        'product.pdpURL': ['https://example.com/product/2'],
                        'product.sku.skuImages': ['https://example.com/image2.jpg'],
                        'product.activity': ['Activity 2'],
                        'product.title': ['Title 2'],
                        'product.categoryHierarchy': ['Category 2'],
                        'product.defaultSku': ['SKU456'],
                        'product.skuAvailabilityMap': ['In Stock'],
                        'currencyCode': ['CAD']
                    }
                }
            ]
        }
        # Mock the get_cached_data method
        mock_get_cached_data.return_value = mock_cached_data

        # Patching PRODUCT_URLS
        with patch('products.views.PRODUCT_URLS', ['https://example.com/products']):
            # Create a request
            request = self.factory.get(self.url)

            # Call the view
            response = self.view(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2) 
            self.assertEqual(response.data[0]['default_sku'],\
                             mock_cached_data['https://example.com/products'][0]['attributes']['product.defaultSku'][0])
            self.assertEqual(response.data[0]['name'],\
                             mock_cached_data['https://example.com/products'][0]['attributes']['product.displayName'][0])
            self.assertEqual(response.data[0]['price'],\
                             mock_cached_data['https://example.com/products'][0]['attributes']['product.price'])
            self.assertEqual(response.data[0]['color'],\
                             mock_cached_data['https://example.com/products'][0]['attributes']['product.sku.color.colorCode'])
            self.assertEqual(response.data[0]['activity'],\
                             mock_cached_data['https://example.com/products'][0]['attributes']['product.activity'])
            self.assertEqual(response.data[0]['title'],\
                             mock_cached_data['https://example.com/products'][0]['attributes']['product.title'][0])
            self.assertEqual(response.data[0]['currency_code'],\
                             mock_cached_data['https://example.com/products'][0]['attributes']['currencyCode'][0]) 
    
    
    # Test for Index error in products
    @patch('products.views.ProductListView.get_cached_data')
    def test_get_products_index_error(self,mock_get_cached_data):
        mock_cached_data = {
            'https://example.com/products': [
                {
                    'attributes': {
                        'product.displayName': [],
                        'product.price': [],
                        'product.sku.color.colorCode': ['Red'],
                        'product.pdpURL': ['https://example.com/product/1'],
                        'product.sku.skuImages': ['https://example.com/image1.jpg'],
                        'product.activity': ['Activity 1'],
                        'product.title': ['Title 1'],
                        'product.categoryHierarchy': ['Category 1'],
                        'product.defaultSku': ['SKU123'],
                        'product.skuAvailabilityMap': ['In Stock'],
                        'currencyCode': ['USD']
                    }
                },
                {
                    'attributes': {
                        'product.displayName': [],
                        'product.price': [],
                        'product.sku.color.colorCode': ['Blue'],
                        'product.pdpURL': ['https://example.com/product/2'],
                        'product.sku.skuImages': ['https://example.com/image2.jpg'],
                        'product.activity': ['Activity 2'],
                        'product.title': ['Title 2'],
                        'product.categoryHierarchy': ['Category 2'],
                        'product.defaultSku': ['SKU456'],
                        'product.skuAvailabilityMap': ['In Stock'],
                        'currencyCode': ['CAD']
                    }
                }
            ]
        }
        # Mock the get_cached_data method
        mock_get_cached_data.return_value = mock_cached_data

        with patch('products.views.PRODUCT_URLS', ['https://example.com/products']):
            # Create a request
            request = self.factory.get(self.url)

            # Call the view
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    # Test for Key error in products
    @patch('products.views.ProductListView.get_cached_data')
    def test_get_products_key_error(self,mock_get_cached_data):
        mock_cached_data = {
            'https://example.com/products': [
                {
                    'attributes': {
                        'product.NAME': ['Product 1'],
                        'product.price': [],
                        'product.sku.color.colorCode': ['Red'],
                        'product.pdpURL': ['https://example.com/product/1'],
                        'product.sku.skuImages': ['https://example.com/image1.jpg'],
                        'product.activity': ['Activity 1'],
                        'product.title': ['Title 1'],
                        'product.categoryHierarchy': ['Category 1'],
                        'product.defaultSku': ['SKU123'],
                        'product.skuAvailabilityMap': ['In Stock'],
                        'currencyCode': ['USD']
                    }
                },
                {
                    'attributes': {
                        'product.NAME': [],
                        'product.price': [],
                        'product.sku.color.colorCode': ['Blue'],
                        'product.pdpURL': ['https://example.com/product/2'],
                        'product.sku.skuImages': ['https://example.com/image2.jpg'],
                        'product.activity': ['Activity 2'],
                        'product.title': ['Title 2'],
                        'product.categoryHierarchy': ['Category 2'],
                        'product.defaultSku': ['SKU456'],
                        'product.skuAvailabilityMap': ['In Stock'],
                        'currencyCode': ['CAD']
                    }
                }
            ]
        }
        # Mock the get_cached_data method
        mock_get_cached_data.return_value = mock_cached_data

        with patch('products.views.PRODUCT_URLS', ['https://example.com/products']):
            # Create a request
            request = self.factory.get(self.url)

            # Call the view
            response = self.view(request)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            
            # Assert the response data contains the expected error message
            expected_message = "KeyError: 'product.displayName'"
            self.assertEqual(response.data, expected_message)
            

    # Test for successful retrieval of products on the first page
    @patch('products.views.ProductListView.get_cached_data')
    def test_get_products_first_page(self,mock_get_cached_data):
        mock_cached_data={'https://example.com/products':[]}
        for i in range(1, 16):
            mock_cached_data['https://example.com/products'].append(
                {
                    'attributes': {
                        'product.displayName': [f'Product {i}'],
                        'product.price': [10.0],
                        'product.sku.color.colorCode': ['Red'],
                        'product.pdpURL': [f'https://example.com/product/ {i}'],
                        'product.sku.skuImages': ['https://example.com/image.jpg'],
                        'product.activity': ['Activity'],
                        'product.title': ['Title'],
                        'product.categoryHierarchy': ['Category'],
                        'product.defaultSku': [f'SKU123{i}'],
                        'product.skuAvailabilityMap': ['In Stock'],
                        'currencyCode': ['USD']
                    }
                })
        # Mock the get_cached_data method
        mock_get_cached_data.return_value = mock_cached_data

        with patch('products.views.PRODUCT_URLS', ['https://example.com/products']):
            # Create a request
            request = self.factory.get(self.url)

            # Call the view
            response = self.view(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 10) # 10 products per page
            

    # Test for successful retrieval of products on the second page
    @patch('products.views.ProductListView.get_cached_data')
    def test_get_products_second_page(self,mock_get_cached_data):
        mock_cached_data={'https://example.com/products':[]}
        for i in range(1, 16):
            mock_cached_data['https://example.com/products'].append(
                {
                    'attributes': {
                        'product.displayName': [f'Product {i}'],
                        'product.price': [10.0],
                        'product.sku.color.colorCode': ['Red'],
                        'product.pdpURL': [f'https://example.com/product/{i}'],
                        'product.sku.skuImages': ['https://example.com/image.jpg'],
                        'product.activity': ['Activity'],
                        'product.title': ['Title'],
                        'product.categoryHierarchy': ['Category'],
                        'product.defaultSku': [f'SKU123{i}'],
                        'product.skuAvailabilityMap': ['In Stock'],
                        'currencyCode': ['USD']
                    }
                })
        # Mock the get_cached_data method
        mock_get_cached_data.return_value = mock_cached_data

        with patch('products.views.PRODUCT_URLS', ['https://example.com/products']):
            # Create a request
            request = self.factory.get(self.url, {'page': 2})

            # Call the view
            response = self.view(request)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 5) # 5 products on the second page


    # Test for None cached products
    @patch('products.views.ProductListView.get_cached_data')
    def test_cached_products_none(self, mock_get_cached_data):
        # Mocking the get_cached_data method to return None
        mock_get_cached_data.return_value = None

        with patch('products.views.PRODUCT_URLS', ['https://example.com/products']):
            # Create a request
            request = self.factory.get(self.url)

            # Call the view
            response = self.view(request)

            # Assert that the response status code is 400
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

            # Assert that the response contains the expected message
            expected_message = "No products received"
            self.assertEqual(response.data, expected_message)


    # Test for cached products
    @patch('products.utils.requests.get')
    @patch('products.utils.cache.set')
    def test_cache_product_data_success(self, mock_cache_set, mock_requests_get):
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "contents": [
                {
                    "mainContent": [
                        {
                            "contents": [
                                {
                                    "records": [
                                        {"product": "abc"}
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

        # Assign mock_response to the return value of requests.get
        mock_requests_get.return_value = mock_response

        # Call the function to be tested
        urls = ['https://example.com/product1', 'https://example.com/product2']
        cache_product_data(urls)

        # Assert that requests.get is called twice with the correct URLs
        mock_requests_get.assert_any_call('https://example.com/product2')
        mock_requests_get.assert_any_call('https://example.com/product2')

        # Assert that cache.set is called twice with the correct arguments
        expected_data = [{"product": "abc"}]
        mock_cache_set.assert_any_call('https://example.com/product1', expected_data)
        mock_cache_set.assert_any_call('https://example.com/product2', expected_data)