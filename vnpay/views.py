from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response

from vnpay.vnpay import VnpayPayment
from datetime import datetime

# Create your views here.
class CreatePayment(APIView):
  def post(self, request, *args, **kwargs):
      order_type = 'other'
      order_id = datetime.now()
      amount = int(request.data['amount'])
      order_desc = 'Nap tien'
      language = 'vn'
      ipaddr = '127.0.0.1:3000'
      # Build URL Payment
      vnp = VnpayPayment(order_type, order_id, order_desc, language, amount, ipaddr)
      # return redirect(vnp.make_payment_url()[0]) 
                
      return Response({'data': vnp.make_payment_url()[0]}, status=200)
    
class PaymentReponse(APIView):
    def get(self, request, format=None):
        input_data = request.GET

        if input_data:
            vnp_transaction_no = input_data.get('vnp_TransactionNo')
            vnp_response_code = input_data.get('vnp_ResponseCode')
            vnp_secure_hash = input_data.get('vnp_SecureHash')
            order_id = input_data.get('vnp_TxnRef')

            response_messages = {
                "00": "Giao dịch thành công",
                "07": "Trừ tiền thành công, giao dịch bị nghi ngờ (liên quan tới lừa đảo, giao dịch bất thường).",
                "09": "Giao dịch không thành công do: Thẻ/Tài khoản của khách hàng chưa đăng ký dịch vụ InternetBanking tại ngân hàng.",
                "10": "Giao dịch không thành công do: Khách hàng xác thực thông tin thẻ/tài khoản không đúng quá 3 lần.",
                "11": "Giao dịch không thành công do: Đã hết hạn chờ thanh toán. Xin quý khách vui lòng thực hiện lại giao dịch.",
                "12": "Giao dịch không thành công do: Thẻ/Tài khoản của khách hàng bị khóa.",
                "13": "Giao dịch không thành công do Quý khách nhập sai mật khẩu xác thực giao dịch (OTP). Xin quý khách vui lòng thực hiện lại giao dịch.",
                "24": "Giao dịch không thành công do: Khách hàng hủy giao dịch.",
                "51": "Giao dịch không thành công do: Tài khoản của quý khách không đủ số dư để thực hiện giao dịch.",
                "65": "Giao dịch không thành công do: Tài khoản của Quý khách đã vượt quá hạn mức giao dịch trong ngày.",
                "75": "Ngân hàng thanh toán đang bảo trì.",
                "79": "Giao dịch không thành công do: KH nhập sai mật khẩu thanh toán quá số lần quy định. Xin quý khách vui lòng thực hiện lại giao dịch.",
                "99": "Các lỗi khác (lỗi còn lại, không có trong danh sách mã lỗi đã liệt kê).",
            }

            message = response_messages.get(
                vnp_response_code, "Mã lỗi không hợp lệ.")
            
            print(message)

            response_data = {
                'code': vnp_response_code,
                'message': message,
                'transaction_no': vnp_transaction_no,
                'response_code': vnp_response_code
            }

            return Response(response_data, status=200)
        return Response("error input_data", status=400)
                
