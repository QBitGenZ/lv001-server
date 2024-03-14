import rest_framework.serializers as serializers
from cart.models import CartDetail
from product.serializers import ProductSerializer


class CartDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartDetail
        fields = ['id', 'product', 'quantity']


class AddCartDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartDetail
        fields = '__all__'
