# users/urls.py
from users.views import RegisterView, verify_view, EmailVerifyView
from .views import ProfileView, ProfileUpdateView
from django.urls import path, reverse_lazy
from users.apps import UsersConfig
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
    LogoutView,
    LoginView,
)

app_name = UsersConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('register/', RegisterView.as_view(), name='register'),
    path('verify_email/', verify_view, name='verify_email'),
    path('verify_email/<str:uidb64>/<str:user_token>/', EmailVerifyView.as_view(), name='incorrect_verify'),

    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset.html',
                                                      email_template_name='users/password_reset_email.html',
                                                      success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password_reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
]
