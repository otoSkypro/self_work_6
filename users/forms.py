# users/forms.py
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from users.models import User
from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'country', 'avatar']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Добавьте настройку полей формы, если необходимо


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserResetPasswordForm(PasswordResetForm):

    class Meta:
        model = User
        fields = ('email',)
