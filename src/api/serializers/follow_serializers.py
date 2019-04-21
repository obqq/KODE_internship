from rest_framework import serializers

from api.models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('user_id', 'email', 'password',)


class FollowerSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = Follow
        fields = ('follower',)


class TargetSerializer(serializers.ModelSerializer):
    target = UserSerializer()

    class Meta:
        model = Follow
        fields = ('target',)
