from django.urls import path, include
from .views import ProductTypeView, ProductView, ProductPkView,ProductByUser,SoldProductView,TotalRevenueByUserAPIView, SearchProductView

urlpatterns = [
    path('types/', ProductTypeView.as_view(), name='product_types'),
    path('types/<uuid:pk>/', ProductTypeView.as_view(), name='product_types'),
    path('', ProductView.as_view(), name='products'),
    path('search/', SearchProductView.as_view(), name='search'),
    path('<uuid:pk>/', ProductPkView.as_view(), name='products'),
    path('images/', include('resource.urls')),
    path('feedbacks/', include('feedback.urls')),
    path('myproducts/', ProductByUser.as_view(), name='my-product'),
    path('myproducts/sold/', SoldProductView.as_view(), name='sold-product'),
    path('myproducts/revenue/', TotalRevenueByUserAPIView.as_view(), name='revenue'),
]
