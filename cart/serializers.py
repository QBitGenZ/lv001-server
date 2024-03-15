import rest_framework.serializers as serializers
from cart.models import CartItem
from product.serializers import ProductSerializer


class CartDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class AddCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
