from rest_framework import serializers
import django.contrib.auth.password_validation as validators

from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'username', 'password')

    def create(self, validated_data):
        user = User.create_user(username=validated_data['username'],
                                password=validated_data['password'])
        user.save()
        return user

    def validate_password(self, password):
        validators.validate_password(password=password, user=User)

        return password
