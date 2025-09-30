import uuid
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    thumbnail = models.URLField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
