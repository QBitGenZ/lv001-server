from django.urls import path
from notification.views import NotificationView, NotificationPkView

urlpatterns = [
    path('', NotificationView.as_view(), name='notification'),
    path('<uuid:pk>/', NotificationPkView.as_view()),
]