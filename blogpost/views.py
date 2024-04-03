from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import BlogPost
from .forms import BlogPostForm


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogpost/post_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogpost/post_detail.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # Увеличение счетчика просмотров
        self.object.views += 1
        self.object.save()
        return response


class BlogPostCreateView(CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost/post_form.html'

    def form_valid(self, form):
        form.instance.slug = form.instance.generate_slug()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blogpost/post_form.html'

    def form_valid(self, form):
        form.instance.slug = form.instance.generate_slug()
        return super().form_valid(form)


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogpost/post_confirm_delete.html'
    success_url = reverse_lazy('blogpost:post_list')


def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    # Увеличение счетчика просмотров
    post.views += 1
    post.save()

    return render(request, 'blogpost/post_detail.html', {'object': post})


def post_edit(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.instance.slug = form.instance.generate_slug()
            form.save()
            return redirect('blogpost:post_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'blogpost/post_form.html', {'form': form})
