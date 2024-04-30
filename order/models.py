import uuid

from django.db import models

from address.models import Address
from product.models import Product
from user_management.models import User


# Create your models here.
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default='Đã đặt hàng')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.id
