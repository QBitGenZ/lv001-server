from django.urls import path

from event.views import EventView, EventPkView

urlpatterns = [
    path('', EventView.as_view(), name='event'),
    path('<uuid:pk>/', EventPkView.as_view(), name='event')
]