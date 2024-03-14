from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from feedback.models import Feedback
from feedback.serializers import ProductFeedbackSerializer


# Create your views here.
class ProductFeedbackView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            product_feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response({'error': 'Đánh giá sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductFeedbackSerializer(product_feedback)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = ProductFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        try:
            product_feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response({'error': 'Đánh giá sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductFeedbackSerializer(instance=product_feedback, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            product_feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response({'error': 'Đánh giá sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product_feedback.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)