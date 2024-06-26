from django.urls import path
from . import views
from .views import CountView, InventoryStatisticsView, InventoryStatisticsAdminView, ProductSalesAPIView,CountUserByStatus,CountProductByStatus, CountEventByStatus, TotalFund, TotalFundByUser

urlpatterns = [
    path('orders/', views.monthly_profit_chart, name='monthly_profit_chart'),
    path('counts/', CountView.as_view(), name='count'),
    path('inventory/', InventoryStatisticsView.as_view(), name='inventory'),
    path('inventory/admin/', InventoryStatisticsAdminView.as_view(), name='inventory'),
    path('my-revenue/', ProductSalesAPIView.as_view(), name='revenue'),
    path('count-user-by-status/', CountUserByStatus.as_view(), name='user-by-status'),
    path('count-product-by-status/', CountProductByStatus.as_view(), name='by-status'),
    path('count-event-by-status/', CountEventByStatus.as_view(), name='by-status'),
    path('total-fund/', TotalFund.as_view(), name='total-fund'),
    path('my-total-fund/', TotalFundByUser.as_view(), name='total-fund-by-user' ),
]
