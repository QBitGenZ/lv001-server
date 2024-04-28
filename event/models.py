from django.db import models
import uuid

from user_management.models import User
from product.models import Product


# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    name = models.CharField(max_length=225)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_user', to_field='username')
    beginAt = models.DateTimeField()
    endAt = models.DateTimeField()
    image = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    status = models.CharField(max_length=255, default='Chưa duyệt')

    def __str__(self):
        return self.name
    
class DonantionProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    
    class Meta:
        unique_together = ('product', 'event')