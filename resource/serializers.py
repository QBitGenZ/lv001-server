from rest_framework import serializers

from resource.models import Image


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['alt', 'src', 'created_at', 'product']


class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['alt', 'src', 'created_at', 'feedback']