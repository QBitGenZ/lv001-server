from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Report
from .serializers import ReportSerializer

class ReportView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = Report.objects.all()
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = ReportSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class ReportPkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ReportSerializer(instance=report)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        try:
            report = Report.objects.get(pk=pk, user=request.user.username)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        data['user'] = request.user.username
        serializer = ReportSerializer(instance=report, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
