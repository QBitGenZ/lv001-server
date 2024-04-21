from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from address.serializers import AddressSerializer
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
    addresses = AddressSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'password', 'is_philanthropist', 'is_seller', 'is_staff',
                  'phone', 'is_female', 'birthday', 'avatar', 'addresses', 'status', 'created_at',
                  'description']

        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'addresses': {'read_only': True},
            'created_at': {
                'read_only':True
            }
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

