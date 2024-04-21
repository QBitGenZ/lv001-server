from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event, DonantionProduct
from event.serializers import EventSerializer, DonantionProductSerializer
from django.db.models import Q
from product.models import Product



# Create your views here.
class EventView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        status_filter = request.query_params.get('status', 'all')
        approval_filter = request.query_params.get('approval', 'all')
        limit = int(limit)
        page = int(page)

        now = timezone.now()
        if status_filter == 'upcoming':
            objects = Event.objects.filter(beginAt__gt=now)
        elif status_filter == 'past':
            objects = Event.objects.filter(endAt__lt=now)
        elif status_filter == 'ongoing':
            objects = Event.objects.filter(beginAt__lte=now, endAt__gte=now)
        else:
            objects = Event.objects.all()

        # Lọc sự kiện dựa trên trạng thái duyệt
        if approval_filter == 'approved':
            objects = objects.filter(status='Đã duyệt')
        elif approval_filter == 'pending':
            objects = objects.filter(status='Chưa duyệt')
        elif status_filter == 'rejected':
            objects = Event.objects.filter(status='Từ chối')
        
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)

        current_page_objects = objects[(page - 1) * limit:page * limit]
        serializer = EventSerializer(current_page_objects, many=True)
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
        if not request.user.is_philanthropist:
            return Response({'error', 'Bạn không phải là nhà từ thiện'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data.copy()
        data['user'] = request.user.username
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data
            }, status.HTTP_201_CREATED)
        else:
            return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class EventPkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(instance=event)
        return Response({
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(instance=event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DonantionProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            limit = request.query_params.get('limit', 10)
            page = request.query_params.get('page', 1)
            limit = int(limit)
            page = int(page)

            
            event_id = kwargs.get('event_id')
            
            objects = DonantionProduct.objects.filter(event_id=event_id)
            total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
            current_page_objects = objects[(page - 1) * limit:page * limit]

            serializer = DonantionProductSerializer(current_page_objects, many=True)
            return Response({
                'data': serializer.data,
                'meta': {
                    'total_pages': total_pages,
                    'current_page': page,
                    'limit': limit,
                    'total': objects.count()
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            serializer = DonantionProductSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                
                product_id = request.data.get('product')
                quantity = request.data.get('quantity')
                product = Product.objects.get(id=product_id)
                product.sold += quantity
                product.save()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, *args, **kwargs):
        try:
            instance = DonantionProduct.objects.get(pk=pk)
            serializer = DonantionProductSerializer(instance=instance, data=request.data, partial=True)
            if serializer.is_valid():
                old_quantity = instance.quantity
                new_quantity = request.data.get('quantity')
                serializer.save()
                product = instance.product
                quantity_change = new_quantity - old_quantity
                product.sold += quantity_change
                product.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DonantionProduct.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance  = DonantionProduct.objects.get(pk=pk)
            product = instance.product
            quantity = instance.quantity
            instance.delete()
            product.sold -= quantity
            product.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DonantionProduct.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class EventSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = int(request.query_params.get('limit', 10))
        page = int(request.query_params.get('page', 1))
        search_query = request.query_params.get('keyword', '')

        objects = Event.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = EventSerializer(current_page_objects, many=True)

        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)