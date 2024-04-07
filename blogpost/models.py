# blogpost/models.py
from django.utils.text import slugify
from django.urls import reverse
from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=555)
    slug = models.SlugField(unique=True, blank=True, max_length=555)  # Увеличиваем max_length
    content = models.TextField()
    preview_image = models.ImageField(upload_to='blogpost/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

    def generate_slug(self):
        """
        Генерация уникального слага для блог-поста на основе заголовка.
        """
        slug = slugify(self.title)
        unique_slug = slug
        counter = 1

        while BlogPost.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1

        return unique_slug[:555]  # Ограничим длину слага до 355 символов

    def save(self, *args, **kwargs):
        """
        Переопределение метода сохранения для генерации и установки слага.
        """
        if not self.slug:
            self.slug = self.generate_slug()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Получение абсолютного URL блог-поста.
        """
        return reverse('blogpost:post_detail', args=[str(self.slug)])

    def __str__(self):
        return self.title
