from rest_framework import serializers

from feedback.models import Feedback
from resource.models import Image
from resource.serializers import FeedbackImageSerializer


class ProductFeedbackSerializer(serializers.ModelSerializer):
    feedback_image = FeedbackImageSerializer(read_only=True, many=True)

    class Meta:
        model = Feedback
        fields = ['id', 'title', 'text', 'user', 'created_at', 'star_number', 'product', 'feedback_image']
