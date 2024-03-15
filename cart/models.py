import uuid

from django.db import models

from product.models import Product
from user_management.models import User


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart',to_field='username')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_in_cart')
    quantity = models.IntegerField()

    def __str__(self):
        return self.product
