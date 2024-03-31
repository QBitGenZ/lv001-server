import uuid

from django.db import models

from user_management.models import User


# Create your models here.
class Notification(models.Model):
    id = models.UUIDField(primary_key=True,auto_created=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', to_field='username')

    def __str__(self):
        return self.title
