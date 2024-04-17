from rest_framework import serializers
from order.models import Order, OrderItem
from product.serializers import ProductSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class AddOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'address', 'payment_method', 'created_at', 'items', 'status')

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
        }
