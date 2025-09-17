import uuid
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)                
    price = models.IntegerField(default=0)                 
    description = models.TextField(blank=True)             
    thumbnail = models.URLField(max_length=500, null = True, blank=True)            
    category = models.CharField(max_length=100, null = True, blank=True)           
    is_featured = models.BooleanField(default=False)      

