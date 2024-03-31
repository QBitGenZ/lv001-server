from rest_framework import serializers

from address import models


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True}
        }