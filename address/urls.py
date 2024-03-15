from django.urls import path

from address.views import AddressView

urlpatterns = [
    path('', AddressView.as_view(), name='address'),
    path('<uuid:pk>/', AddressView.as_view(), name='address'),
]