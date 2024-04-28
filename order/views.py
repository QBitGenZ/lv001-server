from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from order.models import Order, OrderItem
from cart.models import CartItem
from product.models import Product
from order.serializers import OrderSerializer, AddOrderDetailSerializer

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = Order.objects.all()
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)

        current_page_objects = objects[(page - 1) * limit:page * limit]
        serializer = OrderSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'error': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderListPkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(instance=order)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['user'] = request.user.username
        serializer = OrderSerializer(instance=order, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyOrderListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = Order.objects.filter(user=request.user.username).order_by('-created_at')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)

        current_page_objects = objects[(page - 1) * limit:page * limit]
        serializer = OrderSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order, *args, **kwargs):
        try:
            order = Order.objects.get(pk=order)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['order'] = order.id
        serializer = AddOrderDetailSerializer(data=data)
        if serializer.is_valid():
            product_id = data.get('product')
            quantity = int(data.get('quantity'))
            
            product = Product.objects.get(pk=product_id)
            if(product.sold >= product.quantity):
                return Response({'error': 'Sản phẩm đã bán hết'})
            if(product.sold + quantity > product.quantity):
                return Response({'error': 'Sản phẩm không còn đủ số lượng yêu cầu'})
            product.sold += quantity  
            product.save()  
            
            cart_item = CartItem.objects.get(product=product)
            cart_item.quantity -= quantity
            if(cart_item.quantity <= 0):
                cart_item.delete()
            else:
                cart_item.save()
            
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            order_item = OrderItem.objects.get(pk=pk)
        except OrderItem.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        order_item.delete()


