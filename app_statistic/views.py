from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
import calendar

from rest_framework.views import APIView

from order.models import Order
from user_management.models import User


@api_view(['GET'])
def monthly_profit_chart(request):
    from_date_str = request.GET.get('from_date')
    to_date_str = request.GET.get('to_date')

    if from_date_str:
        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
    else:
        from_date = datetime(datetime.now().year, 1, 1)  # Nếu không có từ ngày, lấy từ đầu năm

    if to_date_str:
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')
    else:
        to_date = datetime.now()  # Nếu không có đến ngày, lấy đến ngày hiện tại

    # Khởi tạo một dictionary để lưu trữ lợi nhuận hàng tháng
    monthly_profit = {}

    # Tính toán lợi nhuận cho mỗi tháng trong khoảng thời gian từ from_date đến to_date
    while from_date <= to_date:
        total_profit = Order.objects.filter(
            created_at__year=from_date.year,
            created_at__month=from_date.month
        ).aggregate(total_profit=Sum('items__product__price'))['total_profit'] or 0
        revenue = total_profit * 0.006  # Tính lợi nhuận từ tổng doanh thu với tỷ lệ 0.6%
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

        return Response({'data': {'seller': count_seller, 'buyer': count_buyer, 'philanthropist': count_philanthropist}});