from rest_framework import serializers

from feedback.serializers import ProductFeedbackSerializer
from product.models import ProductType, Product, ProductDetail
from resource.serializers import ProductImageSerializer


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ['id', 'title', 'product', 'text', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer(read_only=True, many=True)
    product_image = ProductImageSerializer(read_only=True, many=True)
    product_feedback = ProductFeedbackSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'price', 'product_type', 'product_detail', 'product_image',
                  'created_at', 'user', 'product_feedback', 'check']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description', 'created_at']


