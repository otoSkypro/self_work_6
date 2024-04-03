from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
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

        while BlogPost.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1

        return unique_slug

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
