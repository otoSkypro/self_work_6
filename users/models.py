# users/models.py
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = models.CharField(max_length=30, verbose_name='Имя пользователя', **NULLABLE)
    phone = models.CharField(max_length=30, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')

    is_active = models.BooleanField(default=False)
    user_token = models.CharField(max_length=255, blank=True, null=True, verbose_name='token')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=150, blank=True)


# Добавляем новую группу пользователей для контент-менеджеров
Group.objects.get_or_create(name='Content Managers')
