from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    price = serializers.JSONField(default=list)
    color = serializers.JSONField(default=list) 
    activity = serializers.JSONField(default=list)
    title = serializers.CharField(required=True)
    default_sku = serializers.CharField(required=True)
    currency_code = serializers.CharField(required=True)
    url = serializers.CharField()
    image_urls = serializers.JSONField(default=list)
    category_hierarchy = serializers.JSONField(default=list)
    availability = serializers.JSONField(default=list)
    class Meta:
        model = Product
        fields = ['default_sku', 'name', 'price', 'color', 'activity', 'title','currency_code','url','image_urls','category_hierarchy', 'availability']
