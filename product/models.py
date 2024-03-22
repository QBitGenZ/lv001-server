import uuid

from django.db import models
from user_management.models import User


# Create your models here.
class ProductType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, default='Chưa duyệt')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_user', to_field='username')
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class ProductDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_detail')

    title = models.CharField(max_length=255)
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
