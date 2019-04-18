from rest_framework import serializers

from api.models import Pitt


class PittSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitt
        fields = ('pitt_id', 'user', 'transcript', 'created_at')
