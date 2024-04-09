# blog/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .forms import PostForm
from .models import Post


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-publication_date']
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_in_content_managers_group = self.request.user.groups.filter(name='Content Managers').exists()
        print("User in Content Managers group:", user_in_content_managers_group)  # Отладочная информация
        context['user_in_content_managers_group'] = user_in_content_managers_group
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        # Получаем объект статьи
        post = get_object_or_404(Post, pk=self.kwargs['pk'])

        # Увеличиваем счетчик просмотров
        post.views += 1
        post.save()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_in_content_managers_group = self.request.user.groups.filter(name='Content Managers').exists()
        print("User in Content Managers group:", user_in_content_managers_group)  # Отладочная информация
        context['user_in_content_managers_group'] = user_in_content_managers_group
        return context


class PostCreateView(UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        return self.request.user.groups.filter(name='Content Managers').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_in_content_managers_group = self.request.user.groups.filter(name='Content Managers').exists()
        print("User in Content Managers group:", user_in_content_managers_group)  # Отладочная информация
        context['user_in_content_managers_group'] = user_in_content_managers_group
        return context


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        return self.request.user.groups.filter(name='Content Managers').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_in_content_managers_group = self.request.user.groups.filter(name='Content Managers').exists()
        print("User in Content Managers group:", user_in_content_managers_group)  # Отладочная информация
        context['user_in_content_managers_group'] = user_in_content_managers_group
        return context
