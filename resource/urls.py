from django.urls import path

from resource.views import ProductImageView

urlpatterns = [
    path('<uuid:pk>/', ProductImageView.as_view(), name='product_images'),
    path('', ProductImageView.as_view(), name='product_images'),
]