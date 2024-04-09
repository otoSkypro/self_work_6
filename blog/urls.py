# blog/urls.py
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),  # Добавляем путь для создания статьи
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),  # Добавляем путь для редактирования статьи
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
