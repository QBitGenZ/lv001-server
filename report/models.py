import uuid

from django.db import models

from user_management.models import User


# Create your models here.
class Report(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports', to_field='username')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
