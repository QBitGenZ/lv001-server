from django.urls import path
from order.views import OrderListView, OrderListPkView, MyOrderListView, OrderDetailView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('myorders/', MyOrderListView.as_view(), name='my-order'),
    path('<uuid:order>/items/', OrderDetailView.as_view(), name='create-item'),
    path('items/<uuid:pk>', OrderDetailView.as_view(), name='delete-item'),
    path('<uuid:pk>/', OrderListPkView.as_view(), name='order-detail'),
]
