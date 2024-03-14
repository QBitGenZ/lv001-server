from django.urls import path

from cart.views import CartDetailView

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('<uuid:pk>', CartDetailView.as_view(), name='cart_detail'),
]