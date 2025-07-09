from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import AuthSerializer, CustomTokenObtainPairSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

User = get_user_model()

class AuthView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        users = User.objects.all()
        serializer = AuthSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Пользователь успешно создан.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Новый view для логина
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Новый view для получения информации о текущем пользователе
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    
@api_view(['GET'])
@permission_classes([AllowAny])  # Или IsAuthenticated если нужна авторизация
def get_users_list(request):
    """Получить список всех доступных пользователей"""
    try:
        # Получаем только доступных пользователей
        users = User.objects.filter(is_available=True, is_active=True)
        
        # Можно добавить фильтрацию
        role = request.GET.get('role')
        city = request.GET.get('city')
        
        if role:
            users = users.filter(role=role)
        if city:
            users = users.filter(city__icontains=city)
            
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
class UserDetailView(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)