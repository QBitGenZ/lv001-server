import hashlib
import hmac
import urllib.parse
import urllib.parse
from lv001_server import settings
from datetime import datetime

def hmacsha512(key, data):
    byteKey = key.encode('utf-8')
    byteData = data.encode('utf-8')
    return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()


class VnpayPayment:
    def __init__(self, order_type, order_id, order_desc, language, payment_amount, ipaddr):
        self.order_type = order_type
        self.order_id = order_id
        self.order_desc = order_desc
        self.language = language
        self.payment_amount = payment_amount
        self.ipaddr = ipaddr
        self.data = self.get_data()
        self.VNPAY_PAYMENT_URL = settings.VNPAY_PAYMENT_URL
        self.VNPAY_HASH_SECRET_KEY = settings.VNPAY_HASH_SECRET_KEY

    def get_data(self):
        data = {}
        data["vnp_Version"] = settings.VNP_VERSION
        data["vnp_Command"] = settings.VNP_COMMAND
        data["vnp_TmnCode"] = settings.VNPAY_TMN_CODE
        data["vnp_Amount"] = int(self.payment_amount * 100)
        data["vnp_CurrCode"] = settings.VNP_CURR_CODE
        data["vnp_TxnRef"] = self.order_id
        data["vnp_OrderInfo"] = self.order_desc
        data["vnp_OrderType"] = self.order_type
        data["vnp_Locale"] = "vn"
        data["vnp_CreateDate"] = datetime.now().strftime("%Y%m%d%H%M%S")
        data["vnp_IpAddr"] = self.ipaddr
        data["vnp_ReturnUrl"] = settings.VNPAY_RETURN_URL

        return data

    def get_secure_hash(self):
        # Sort dictionary items alphabetically by key (Python will use default alphabetical sorting)
        sorted_data = dict(sorted(self.data.items()))

        queryString = ""
        for key, val in sorted_data.items():
            queryString += f"{key}={urllib.parse.quote_plus(str(val))}&"

        queryString = queryString[:-1]

        return hmacsha512(self.VNPAY_HASH_SECRET_KEY, queryString)

    def make_payment_url(self):
        hashValue = self.get_secure_hash()
        url =self.VNPAY_PAYMENT_URL + "?" + urllib.parse.urlencode(self.data) + '&vnp_SecureHash=' + hashValue
        return url, hashValue
    
