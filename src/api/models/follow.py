from django.db import models
from .user import User

class Follow(models.Model):
    target = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='targets', on_delete=models.CASCADE)