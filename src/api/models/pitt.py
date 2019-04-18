import uuid

from django.db import models

from .user import User


class Pitt(models.Model):
    pitt_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='audio/')
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
