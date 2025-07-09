from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    phone_number = models.CharField(max_length=9)
    avatar = models.ImageField(upload_to='avatars/' , blank=True, null=True)
    is_vip = models.BooleanField(default=False)
    city = models.CharField(max_length=100)
    desc = models.TextField(max_length=300)
    skills = models.TextField(max_length=500)
    is_available = models.BooleanField(default=True)
    role = models.CharField(max_length=200)
    rating = models.FloatField(default=0)
    def __str__(self):
        return f"{self.username} {self.role}"
    
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = "Пользователи"