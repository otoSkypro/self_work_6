# catalog/services.py
from django.core.cache import cache
from .models import Category


def get_cached_categories():
    # Попытаемся получить категории из кеша
    categories = cache.get('categories')

    if not categories:
        # Если категории отсутствуют в кеше, получим их из базы данных
        categories = Category.objects.all()

        # Кешируем категории на 1 час
        cache.set('categories', categories, 3600)

    return categories
