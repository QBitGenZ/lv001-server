from rest_framework import serializers

from report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True}
        }