# blogpost/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostDetailView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView
)

app_name = 'blogpost'

urlpatterns = [
    path('', BlogPostListView.as_view(), name='post_list'),
    path('create/', BlogPostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('<slug:slug>/edit/', BlogPostUpdateView.as_view(), name='post_edit'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
