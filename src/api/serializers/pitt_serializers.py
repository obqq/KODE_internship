from rest_framework import serializers

from api.models import Pitt


class PittSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="user.username")

    class Meta:
        model = Pitt
        fields = ('pitt_id', 'username', 'audio', 'transcript', 'created_at')
