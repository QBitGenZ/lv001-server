from django.urls import path
from .views import CreatePayment, PaymentReponse

urlpatterns = [
    path('create-url/', CreatePayment.as_view()),
    path('payment_response/', PaymentReponse.as_view()),
]
