from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
import calendar

from rest_framework.views import APIView

from order.models import Order
from user_management.models import User
from product.models import Product
from django.db.models import Q, F, ExpressionWrapper, Sum
from product.serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


@api_view(['GET'])
def monthly_profit_chart(request):
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

    if from_date_str:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
    else:
        from_date = datetime(datetime.now().year, 1, 1) 

    if to_date_str:
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
    else:
        to_date = datetime.now() 

    monthly_profit = {}
    
    while from_date <= to_date:
        total_profit = Order.objects.filter(
            created_at__year=from_date.year,
            created_at__month=from_date.month
        ).aggregate(total_profit=Sum('items__product__price'))['total_profit'] or 0
        revenue = total_profit * 0.006  
        monthly_profit[from_date.strftime('%Y-%m')] = revenue
        from_date = from_date + timedelta(days=calendar.monthrange(from_date.year, from_date.month)[1])

    return Response(
        {'data': monthly_profit},
        status=status.HTTP_200_OK
    )

class CountView(APIView):
    def get(self, request):
        count_seller = User.objects.filter(is_seller=True).count()
        count_buyer = User.objects.filter(is_staff=False).count()
        count_philanthropist = User.objects.filter(is_philanthropist=True).count()

        return Response({'data': {'seller': count_seller, 'buyer': count_buyer, 'philanthropist': count_philanthropist}})
    
class InventoryStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(user=request.user).annotate(remaining=F('quantity') - F('sold')).filter(remaining__gt=0).order_by('name')
        
        total_inventory = Product.objects.aggregate(total_inventory=Sum('quantity'))['total_inventory']
        
        total_new_inventory = Product.objects.filter(degree__gt=0).aggregate(total_new_inventory=Sum('quantity'))['total_new_inventory']
        
        new_inventory_ratio = (total_new_inventory / total_inventory) * 100 if total_inventory > 0 else 0
        
        product_serializer = ProductSerializer(products, many=True)
        
        return Response({
            'data': product_serializer.data,
            'meta': {
                'total_inventory': total_inventory,
                'total_new_inventory': total_new_inventory,
                'new_inventory_ratio': new_inventory_ratio,
                'remaining_products_count': len(products)
            },
        }, status=status.HTTP_200_OK)