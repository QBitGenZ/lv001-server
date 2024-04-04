from django.urls import path

from .views import ReportView, ReportPkView

urlpatterns = [
    path('', ReportView.as_view(), name='report'),
    path('<uuid:pk>/', ReportPkView.as_view(), name='report-pk'),
]