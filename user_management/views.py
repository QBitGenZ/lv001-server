from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user_management.models import User
from user_management.serializers import UserSerializer, AdminUserSerializer, LoginSerializer, ChangePasswordSerializer


# Create your views here.
class AdminUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = User.objects.filter(is_staff=True)
        
        
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = AdminUserSerializer(current_page_objects, many=True)
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
        if request.user.is_superuser:
            serializer = AdminUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        if request.user.is_superuser:
            username = request.query_params.get('username')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response('Data does not exist', status=status.HTTP_404_NOT_FOUND)

            serializer = AdminUserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.user.is_staff:
                serializer = AdminUserSerializer(request.user, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            username = request.query_params.get('username')
            user = User.objects.get(username=username)
            user.delete()
            return Response('User deleted', status=status.HTTP_200_OK)
        else:
            return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)


class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        is_seller = request.query_params.get('is_seller', None)
        username = request.query_params.get('username', None)
        is_philanthropist = request.query_params.get('is_philanthropist', None)

        if username:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            limit = request.query_params.get('limit', 10)
            page = request.query_params.get('page', 1)
            limit = int(limit)
            page = int(page)

            objects = User.objects.filter()
            
            
            if is_seller:
                objects = objects.filter(is_seller=True)
            if is_philanthropist:
                objects = objects.filter(is_philanthropist=True)
            
            total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
            current_page_objects = objects[(page - 1) * limit:page * limit]

            serializer = UserSerializer(current_page_objects, many=True)
            return Response({
                'data': serializer.data,
                'meta': {
                    'total_pages': total_pages,
                    'current_page': page,
                    'limit': limit,
                    'total': objects.count()
                }
            }, status=status.HTTP_200_OK)
        
    def put(self, request, *args, **kwargs):
        serializers = UserSerializer(request.user, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if request.user.is_superuser:
            username = request.query_params.get('username')
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response('User not found', status=status.HTTP_404_NOT_FOUND)
            user.delete()
            return Response('User deleted',status=status.HTTP_204_NO_CONTENT)
        else:
            request.user.delete()
            return Response('User deleted', status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            user_serializer = UserSerializer(user)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'is_philanthropist': user_serializer.data['is_philanthropist'],
                    'is_staff': user_serializer.data['is_staff'],
                    'status': user_serializer.data['status'],
                })
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        logout(request)
        return Response('Logged out', status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


class ChangeStatusView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def put(self, request, username, *args, **kwargs):
        user = User.objects.get(username=username)
        serializers = UserSerializer(user, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({'error': 'Mật khẩu cũ không chính xác'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_password(new_password, user=user)
            except ValidationError as e:
                return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            update_last_login(None, user)  # Update last login to avoid user logout
            return Response('Password changed successfully', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)