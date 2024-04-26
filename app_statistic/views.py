from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
import calendar

from rest_framework.views import APIView

from order.models import Order, OrderItem
from event.models import Event
from user_management.models import User
from product.models import Product
from django.db.models import Q, F, ExpressionWrapper, Sum,functions
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
    
class InventoryStatisticsAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, *args, **kwargs):
        products = Product.objects.annotate(remaining=F('quantity') - F('sold')).filter(remaining__gt=0).order_by('name')
        
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
        
class InventoryStatisticsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        products = Product.objects.filter(user=user).annotate(remaining=F('quantity') - F('sold')).filter(remaining__gt=0).order_by('name')
        
        total_inventory = products.aggregate(total_inventory=Sum('quantity'))['total_inventory']
        
        total_new_inventory = products.filter(degree__gt=0).aggregate(total_new_inventory=Sum('quantity'))['total_new_inventory']
        
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
        
class ProductSalesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()

        if 'start_date' in request.query_params:
            start_date = datetime.strptime(request.query_params['start_date'], '%Y-%m-%d')
        if 'end_date' in request.query_params:
            end_date = datetime.strptime(request.query_params['end_date'], '%Y-%m-%d')

        user_products = Product.objects.filter(user=request.user)

        sales_by_month = OrderItem.objects.filter(
            product__in=user_products,
            order__created_at__range=(start_date, end_date)
        ).annotate(
            month=functions.TruncMonth('order__created_at')
        ).values('month').annotate(
            total_sold=Sum('quantity'),
            revenue=Sum(F('quantity') * F('product__price'))
        )
        
        sales_by_month_dict = {}
        for sale in sales_by_month:
            sale['month'] = sale['month'].replate(date=1)
            sales_by_month_dict[sale['month']] = {
                'total_sold': sale['total_sold'] or 0,
                'revenue': sale['revenue'] or 0
            }
            
        print(sales_by_month)
        
        final_sales_by_month = []
        current_date = start_date.replace(day=1)
        while current_date <= end_date:
            if current_date not in sales_by_month_dict:
                sales_by_month_dict[current_date] = {'total_sold': 0, 'revenue': 0}
            final_sales_by_month.append({
                'month': current_date,
                'total_sold': sales_by_month_dict[current_date]['total_sold'],
                'revenue': sales_by_month_dict[current_date]['revenue']
            })
            current_date = current_date + timedelta(days=32)
            current_date = current_date.replace(day=1)
            
        print(final_sales_by_month)

        return Response({'data': final_sales_by_month}, status=status.HTTP_200_OK)
    
class CountUserByStatus(APIView):
    def get(self, request):
        query = request.query_params.get('status', None)
        objects = User.objects.filter(status=query)
        objects = objects.filter(is_philanthropist=True)
        return Response({'data':objects.count()}, status=status.HTTP_200_OK)
    
class CountProductByStatus(APIView):
    def get(self, request):
        query = request.query_params.get('status', None)
        objects = Product.objects.filter(status=query)
        return Response({'data':objects.count()}, status=status.HTTP_200_OK)
    
class CountEventByStatus(APIView):
    def get(self, request):
        query = request.query_params.get('status', None)
        objects = Event.objects.filter(status=query)
        return Response({'data':objects.count()}, status=status.HTTP_200_OK)

            