# blogpost/forms.py
from django import forms
from .models import BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview_image', 'is_published']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Проверка, есть ли поле slug в форме перед изменением виджета
        if 'slug' in self.fields:
            self.fields['slug'].widget = forms.HiddenInput()
