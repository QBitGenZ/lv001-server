from django.urls import path

from feedback.views import ProductFeedbackView
from resource.views import FeedbackImageView

urlpatterns = [
    path('<uuid:pk>/', ProductFeedbackView.as_view(), name='product_feedbacks'),
    path('', ProductFeedbackView.as_view(), name='product_feedbacks'),
    path('images/', FeedbackImageView.as_view(), name='feedback_images'),
    path('images/<uuid:pk>/', FeedbackImageView.as_view(), name='feedback_images'),
]

