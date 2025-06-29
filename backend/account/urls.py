from django.urls import path
from .views import AuthView, LoginView, MeView

urlpatterns = [
    path('register/', AuthView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
]