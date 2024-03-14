from django.urls import path
from .views import ProductTypeView, ProductView, ProductDetailView, ProductImageView

urlpatterns = [
    path('types', ProductTypeView.as_view(), name='product_types'),
    path('types/<uuid:pk>/', ProductTypeView.as_view(), name='product_types'),
    path('', ProductView.as_view(), name='products'),
    path('<uuid:pk>/', ProductView.as_view(), name='products'),
    path('details/<uuid:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('details/', ProductDetailView.as_view(), name='product_details'),
    path('images/<uuid:pk>/', ProductImageView.as_view(), name='product_images'),
    path('images/', ProductImageView.as_view(), name='product_images'),
]
