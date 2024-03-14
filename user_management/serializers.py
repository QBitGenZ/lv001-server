from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from user_management.models import User


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'password', 'is_superuser', 'is_staff', 'phone', 'birthday',
                  'avatar', 'is_female']

        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['is_staff'] = True
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'password', 'is_philanthropist', 'is_seller',
                  'phone', 'is_female', 'birthday', 'avatar']

        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

