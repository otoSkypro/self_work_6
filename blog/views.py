from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import ArticleForm
from blog.models import Article
from blog.services import get_article_cache
from config import settings


class ArticleListView(ListView):
    model = Article

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if settings.CACHE_ENABLED:
            context_data['article_list'] = get_article_cache()
        else:
            context_data['article_list'] = Article.objects.all()
        return context_data


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    permission_required = 'blog.add_article'
    success_url = reverse_lazy('blog:article_list')


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.count_views += 1
        self.object.save()
        return self.object


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    permission_required = 'blog.change_article'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('pk')])


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    permission_required = 'blog.delete_article'
    success_url = reverse_lazy('blog:article_list')
