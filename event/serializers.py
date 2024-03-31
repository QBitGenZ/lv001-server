from rest_framework import serializers

from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
        }

