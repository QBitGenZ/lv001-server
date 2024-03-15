from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from address.models import Address
from address.serializers import AddressSerializer


# Create your views here.
class AddressView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)

        return Response({
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        try:
            address = Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return Response({
                'error': 'Địa chỉ không tồn tại',
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(instance=address, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            address = Address.objects.get(pk=pk)
        except Address.DoesNotExist:
            return Response({
                'error': 'Địa chỉ không tồn tại',
            }, status=status.HTTP_404_NOT_FOUND)

        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

