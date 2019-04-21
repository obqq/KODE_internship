import uuid

from django.db import models

from .user import User


def user_directory_path(instance, filename):
    return f'{instance.user.user_id}/{instance.pitt_id}_{filename}'


class Pitt(models.Model):
    pitt_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, related_name='pitts', on_delete=models.CASCADE)
    audio = models.FileField(upload_to=user_directory_path)
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
