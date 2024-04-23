from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from feedback.models import Feedback
from product.models import ProductType, Product, ProductDetail
from product.serializers import ProductTypeSerializer, ProductSerializer, ProductImageSerializer, ProductDetailSerializer, ProductFeedbackSerializer
from resource.models import Image
from django.db import models
from django.db.models import Q, F, ExpressionWrapper, Sum


# Create your views here.
class ProductTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = ProductType.objects.all()
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = ProductTypeSerializer(current_page_objects, many=True)
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

        serializer = ProductTypeSerializer(instance=product_type, data=request.data, partial=True)

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
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        degree_filter = request.query_params.get('degree', 'all')
        size_filter = request.query_params.get('size', 'all')
        product_type_filter = request.query_params.get('product_type', 'all')
        gender = request.query_params.get('gender', 'all')
        limit = int(limit)
        page = int(page)

        objects = Product.objects.all()
        
        if degree_filter != 'all':
            objects = objects.filter(degree=degree_filter)
            
        if size_filter != 'all':
            objects = objects.filter(size=size_filter)
        if product_type_filter != 'all':
            objects = objects.filter(product_type__name=product_type_filter)
        if gender != 'all':
            objects = objects.filter(gender=gender)
        
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = ProductSerializer(current_page_objects, many=True)
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

        product_serializer = ProductSerializer(data=data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({
                'data': product_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product_serializer = ProductSerializer(instance=product, data=request.data, partial=True)
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

class ProductByUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = Product.objects.filter(user=request.user.username)
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = ProductSerializer(current_page_objects, many=True)
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
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ProductPkView(APIView):
    
    def get(self, request, pk, *args, **kwargs):
        try:
            product_detail = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product_detail)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request, pk, *args, **kwargs):
        try:
            product_detail = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(instance=product_detail, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        try:
            product_detail = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Sản phẩm không tồn tại'}, status=status.HTTP_404_NOT_FOUND)

        product_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SoldProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = Product.objects.filter(user=request.user.username, sold__gt = 0).order_by('name')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = ProductSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

class TotalRevenueByUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        username = request.user.username
        total_revenue = Product.objects.filter(sold__gt=0, user__username=username).aggregate(total_revenue=Sum(ExpressionWrapper(F('price') * F('sold'), output_field=models.FloatField())))['total_revenue']
        
        return Response(
            {'data': total_revenue},
            status=status.HTTP_200_OK
        )

class SearchProductView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get('keyword', '')
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)


        products = Product.objects.filter(
            Q(name__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(size__icontains=keyword)  
        )

        total_pages = len(products) // limit + (1 if len(products) % limit > 0 else 0)
        current_page_products = products[(page - 1) * limit:page * limit]

        serializer = ProductSerializer(current_page_products, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': products.count()
            }
        }, status=status.HTTP_200_OK)
        
class SearchProductByUserView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        keyword = request.query_params.get('keyword', '')
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)


        products = Product.objects.filter(
            Q(user=request.user) & (
                Q(name__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(size__icontains=keyword)
            )
        )

        total_pages = len(products) // limit + (1 if len(products) % limit > 0 else 0)
        current_page_products = products[(page - 1) * limit:page * limit]

        serializer = ProductSerializer(current_page_products, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': products.count()
            }
        }, status=status.HTTP_200_OK)
