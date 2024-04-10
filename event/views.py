from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event
from event.serializers import EventSerializer
from django.db.models import Q


# Create your views here.
class EventView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        search_query = request.query_params.get('search', '')
        limit = int(limit)
        page = int(page)

        objects = Event.objects.all()
        
        if search_query and search_query.strip():
            objects = objects.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(status__icontains=search_query) 
            )
        
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


