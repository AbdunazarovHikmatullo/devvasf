from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class AuthSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'avatar',
            'is_vip',
            'city',
            'desc',
            'skills',
            'is_available',
            'role',
            'rating',
            'password',
            'password2',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

# Новый сериализатор для логина
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Добавляем информацию о пользователе в ответ
        data['user'] = AuthSerializer(self.user).data
        return data

# Сериализатор для получения информации о пользователе
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'avatar',
            'is_vip',
            'city',
            'desc',
            'skills',
            'is_available',
            'role',
            'rating',
        ]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'email', 'phone_number', 'avatar', 'is_vip',
            'city', 'desc', 'skills', 'is_available', 
            'role', 'rating'
        ]
        # Исключаем чувствительные данные
        extra_kwargs = {
            'email': {'write_only': True},  # Скрываем email в публичном списке
            'phone_number': {'write_only': True},  # Скрываем телефон
        }

# Можно создать отдельный serializer для публичного списка
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 
            'avatar', 'is_vip', 'city', 'desc', 'skills', 
            'is_available', 'role', 'rating'
        ]