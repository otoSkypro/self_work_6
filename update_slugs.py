# update_slugs.py
import os
import django
from django.utils.text import slugify

# Установка переменной окружения для настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_Web_Store.settings')
django.setup()

from blogpost.models import BlogPost  # Замените 'blogpost' на имя вашего приложения


def update_slugs():
    blogposts = BlogPost.objects.all()

    for post in blogposts:
        # Генерация slug для каждого блог-поста
        slug = slugify(post.title)
        post.slug = slug
        post.save()

    print("Slugs have been updated successfully.")


if __name__ == "__main__":
    update_slugs()
