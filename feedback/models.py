import uuid

from django.db import models

from product.models import Product
from user_management.models import User

# Create your models here.
class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    star_number = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_user', to_field='username')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='product_feedback')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title