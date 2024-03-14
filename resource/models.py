import uuid

from django.db import models

from product.models import Product


# Create your models here.
class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    alt = models.CharField(max_length=225)
    src = models.ImageField(upload_to='uploads/%Y/%m/%d', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image',
                                null=True, blank=True)

    def __str__(self):
        return self.alt