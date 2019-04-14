import unicodedata
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(models.Model):
    username_validator = UnicodeUsernameValidator()

    user_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    username = models.CharField(
        max_length=128,
        unique=True,
        help_text=(f'Required. 128 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        }
    )
    password = models.CharField(('password'), max_length=128)


    REQUIRED_FIELDS = ['username', 'password']


    def _create_user(self, username, password):
        username = self.normalize_username(username)
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password):
        return self._create_user(username, password)

    def delete_user(self, user, raw_password):
        check = user.check_password(raw_password)

        if check:
            user.delete()
            return check

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_username(self):
        return self.username

    # to be implemented

    def follow(self, user):
        pass

    def unfollow(self, user):
        pass

    def is_following(self, user):
        pass

    def is_followed_by(self, user):
        pass

    def pitts(self):
        pass

    def follows(self):
        pass

    def __str__(self):
        return self.get_username()


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)


class Pitt(models.Model):
    pitt_id = models.CharField(max_length=128, default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='audio/')
    transcript = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
