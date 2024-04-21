from django.urls import path

from event.views import EventView, EventPkView, DonantionProductView, EventSearchView

urlpatterns = [
    path('', EventView.as_view(), name='event'),
    path('search/', EventSearchView.as_view(), name='search'),
    path('<uuid:pk>/', EventPkView.as_view(), name='event'),
    path('<uuid:event_id>/donation_products/', DonantionProductView.as_view(), name='donation-product-list'),
]