# catalog/models.py
from users.models import User
from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.created_at}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    version_number = models.CharField(max_length=20)
    version_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.product.name} - {self.version_number} - {self.version_name}'


class Product(models.Model):
    MODERATION_CHOICES = [
        ('pending', 'На модерации'),
        ('approved', 'Одобрено'),
        ('rejected', 'Отклонено'),
    ]

    PUBLISH_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'Архивирован'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, verbose_name='пользователь')
    publish_status = models.CharField(max_length=20, choices=PUBLISH_CHOICES, default='draft', verbose_name='Статус публикации')
    moderation_status = models.CharField(max_length=20, choices=MODERATION_CHOICES, default='pending', verbose_name='Статус модерации')

    def is_owner(self, user):
        return self.user == user

    def __str__(self):
        return self.name