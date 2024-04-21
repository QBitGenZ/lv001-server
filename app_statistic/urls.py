from django.urls import path
from . import views
from .views import CountView, InventoryStatisticsView

urlpatterns = [
    path('orders/', views.monthly_profit_chart, name='monthly_profit_chart'),
    path('counts/', CountView.as_view(), name='count'),
    path('inventory/', InventoryStatisticsView.as_view(), name='inventory'),
]
