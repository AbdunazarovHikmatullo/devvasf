from django.urls import path
from .views import AuthView, LoginView, MeView  , UserDetailView
from . import views

urlpatterns = [
    path('register/', AuthView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('users/', views.get_users_list, name='users' ),
    path('users/<str:username>/', UserDetailView.as_view()),
]