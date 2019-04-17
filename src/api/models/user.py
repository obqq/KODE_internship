import unicodedata
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from api.tasks import send_email


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
    email = models.EmailField(blank=True, null=True, max_length=256)
    first_name = models.CharField(blank=True, null=True, max_length=128)
    last_name = models.CharField(blank=True, null=True, max_length=128)
    password = models.CharField(('password'), max_length=128)

    REQUIRED_FIELDS = ['username', 'password']

    @classmethod
    def create_user(cls, username, password, **kwargs):
        username = cls.normalize_username(username)
        user = User(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    @classmethod
    def delete_user(cls, user, raw_password):
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

    def follow(self, target):
        self.targets.create(target=target, follower=self)

        send_email.apply_async((f'Dear {target.username}. {self.username} is now following you.',))
        return True

    def unfollow(self, target):
        old_follow = self.targets.get(target=target)
        old_follow.delete()
        return True

    def is_following(self, target):
        try:
            self.targets.get(target=target)
            return True
        except:
            pass

    def __str__(self):
        return self.username
