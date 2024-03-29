from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem
from cart.serializers import CartDetailSerializer, AddCartDetailSerializer
from product.models import Product


# Create your views here
class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart_detail = CartItem.objects.filter(user=request.user)
        serializer = CartDetailSerializer(cart_detail, many=True)
        return Response({
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        serializer = AddCartDetailSerializer(data=data)

        if serializer.is_valid():
            product_id = serializer.validated_data['product']
            user = request.user
            quantity = serializer.validated_data.get('quantity', 1)

            # Check if the product already exists in the user's cart
            try:
                cart_item = CartItem.objects.get(user=user, product=product_id)
                # Update the quantity
                cart_item.quantity += quantity
                cart_item.save()
                return Response({
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            except CartItem.DoesNotExist:
                # If the product does not exist in the cart, create a new entry
                serializer.save()
                return Response({
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            cart_detail = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({
                'error': 'Chi tiết giỏ hàng không tồn tại'
            }, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['user'] = request.user.username

        serializer = AddCartDetailSerializer(instance=cart_detail, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            cart_detail = CartItem.objects.get(pk=pk)
        except CartItem.DoesNotExist:
            return Response({
                'error': 'Chi tiết giỏ hàng không tồn tại'
            }, status=status.HTTP_404_NOT_FOUND)
        cart_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






