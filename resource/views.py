from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from resource.models import Image
from resource.serializers import ProductImageSerializer, FeedbackImageSerializer


# Create your views here.
class ProductImageView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            feedback_images = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({'error': 'Ảnh sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductImageSerializer(feedback_images)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            feedback_images = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({'error': 'Ảnh sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductImageSerializer(instance=feedback_images, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            feedback_images = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({'error': 'Ảnh sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        feedback_images.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FeedbackImageView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            product_images = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({'error': 'Ảnh sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackImageSerializer(product_images)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = FeedbackImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            product_image = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({'error': 'Ảnh sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FeedbackImageSerializer(instance=product_image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            product_image = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response({'error': 'Ảnh sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
