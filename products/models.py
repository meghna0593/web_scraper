from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.JSONField(models.IntegerField(), default=list)
    color = models.JSONField(default=list) 
    url = models.URLField()
    image_urls = models.JSONField(default=list)  
    activity = models.JSONField(default=list)
    title = models.CharField(max_length=255)
    category_hierarchy = models.JSONField(default=list) 
    default_sku = models.CharField(max_length=100)
    availability = models.JSONField(default=list) 
    currency_code = models.CharField(max_length=100)

    class Meta:
        managed = False