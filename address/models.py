import uuid

from django.db import models

from user_management.models import User


# Create your models here.
class Address(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', to_field='username')

    def __str__(self):
        return self.address
