from rest_framework import serializers

from event.models import Event, DonantionProduct
from product.serializers import ProductSerializer

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
        }

class DonantionProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = DonantionProduct
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
        }
        
class CreateDonantionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonantionProduct
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
        }
