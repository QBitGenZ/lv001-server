from rest_framework import serializers

from product.models import ProductType, Product, ProductDetail
from resource.models import Image


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['alt', 'src', 'created_at', 'product']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ['id', 'title', 'product', 'text', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    product_detail = ProductDetailSerializer(read_only=True, many=True)
    product_image = ProductImageSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'quantity', 'price', 'product_type', 'product_detail', 'product_image',
                  'created_at', 'user']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'description', 'created_at']
