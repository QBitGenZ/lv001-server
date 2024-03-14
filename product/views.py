from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from feedback.models import Feedback
from product.models import ProductType, Product, ProductDetail
from product.serializers import ProductTypeSerializer, ProductSerializer, ProductImageSerializer, \
    ProductDetailSerializer, ProductFeedbackSerializer
from resource.models import Image


# Create your views here.
class ProductTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        product_types = ProductType.objects.all()

        paginator = Paginator(product_types, limit)

        try:
            product_types_page = paginator.page(page)
        except EmptyPage:
            product_types_page = paginator.page(paginator.num_pages)

        serializer = ProductTypeSerializer(product_types_page, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):

        serializer = ProductTypeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data
            },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            product_type = ProductType.objects.get(pk=pk)
        except ProductType.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductTypeSerializer(instance=product_type, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data
            },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            product_type = ProductType.objects.get(pk=pk)
        except ProductType.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductView(APIView):
    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        product = Product.objects.all().order_by('created_at')

        paginator = Paginator(product, limit)

        try:
            products_page = paginator.page(page)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        serializer = ProductSerializer(products_page, many=True)
        return Response(
            {
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        product_serializer = ProductSerializer(data=data)
        if product_serializer.is_valid():
            product_serializer.save()

            return Response({
                'data': product_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(
            {'error': product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product_serializer = ProductSerializer(instance=product, data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({
                'data': product_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': product_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            product_detail = ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            return Response({'error': 'Chi tiết sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product_detail)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            product_detail = ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            return Response({'error': 'Chi tiết sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(instance=product_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            product_detail = ProductDetail.objects.get(pk=pk)
        except ProductDetail.DoesNotExist:
            return Response({'error': 'Chi tiết sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

