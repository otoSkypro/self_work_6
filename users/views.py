# users/views.py
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, LogoutView as DjangoLogoutView
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.contrib.auth.views import LoginView
from mailing_service.models import Mailing
from users.models import User, UserProfile
from users.forms import UserRegisterForm
from users.utils import register_confirm
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserProfileForm
from django.conf import settings
from django.urls import reverse
from django.views import View


class ModeratorDashboardView(PermissionRequiredMixin, View):
    # Устанавливаем необходимые разрешения для модератора
    permission_required = 'users.can_view_dashboard'

    def get(self, request):
        # Получаем список всех пользователей
        users = User.objects.all()
        # Получаем список всех рассылок
        mailings = Mailing.objects.all()
        # Передаем значения в контекст шаблона
        return render(request, 'users/moderator_dashboard.html', {'users': users, 'mailings': mailings, 'has_perm_can_view_dashboard': request.user.has_perm('users.can_view_dashboard')})

    def post(self, request):
        # Получаем список всех пользователей
        users = User.objects.all()
        # Получаем список всех рассылок
        mailings = Mailing.objects.all()

        # Проверяем, был ли передан POST-запрос для блокировки пользователя
        if 'block_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.is_active = False
            user.save()
            # После блокировки пользователя перенаправляем на страницу с пользователями
            return redirect(reverse('users:moderator_dashboard'))

        # Проверяем, был ли передан POST-запрос для разблокировки пользователя
        elif 'unblock_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.is_active = True
            user.save()
            # После разблокировки пользователя перенаправляем на страницу с пользователями
            return redirect(reverse('users:moderator_dashboard'))

        # Проверяем, был ли передан POST-запрос для блокировки рассылки
        elif 'block_mailing' in request.POST:
            mailing_id = request.POST.get('mailing_id')
            mailing = get_object_or_404(Mailing, id=mailing_id)
            mailing.status = 'blocked'
            mailing.save()
            # После блокировки рассылки перенаправляем на страницу с рассылками
            return redirect(reverse('users:moderator_dashboard'))

        # Проверяем, был ли передан POST-запрос для разблокировки рассылки
        elif 'unblock_mailing' in request.POST:
            mailing_id = request.POST.get('mailing_id')
            mailing = get_object_or_404(Mailing, id=mailing_id)
            mailing.status = 'started'
            mailing.save()
            # После разблокировки рассылки перенаправляем на страницу с рассылками
            return redirect(reverse('users:moderator_dashboard'))

        return render(request, 'users/moderator_dashboard.html', {'users': users, 'mailings': mailings})


class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            form = UserProfileForm(instance=user_profile)
            return render(request, self.template_name, {'form': form, 'user': request.user})
        else:
            return redirect('users:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()
                # Обновляем контекст с новыми данными пользователя
                return render(request, self.template_name, {'form': form, 'user': request.user})
            else:
                print(form.errors)
                return render(request, self.template_name, {'form': form, 'user': request.user})
        else:
            return redirect('users:login')


class ProfileUpdateView(View):
    template_name = 'users/profile_update.html'

    def get(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(instance=user_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            # Обновляем соответствующие поля в User
            request.user.username = form.cleaned_data['username']
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.phone = form.cleaned_data['phone_number']
            request.user.country = form.cleaned_data['country']
            request.user.avatar = form.cleaned_data['avatar']
            request.user.save()

            return render(request, 'users/profile.html', {'form': form, 'user': request.user})
        return render(request, self.template_name, {'form': form})


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verify_email')

    def form_valid(self, form, *args, **kwargs):
        new_user = form.save()
        new_user.user_token = token_generator.make_token(new_user)
        form.save()
        register_confirm_ = register_confirm(self.request, user=new_user)
        if not new_user.is_active:
            send_mail(
                subject="Подтверждение почты",
                message=register_confirm_['message'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[new_user.email]
            )
        return super().form_valid(form)


class EmailVerifyView(View):
    success_url = 'users/verified_email.html'

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None
        return user

    def get(self, request, uidb64, user_token):
        user = self.get_user(uidb64)

        if user is not None and user.user_token == user_token:
            user.is_active = True
            user.is_staff = True
            user.save()

            return render(request, 'users/verified_email.html')
        else:
            return render(request, 'users/incorrect_verify.html')


def verify_view(request):
    return render(request, 'users/verify_email.html')


class UserPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class PasswordResetDoneView(TemplateView):
    template_name = 'users/password_reset_done.html'


class PasswordResetCompleteView(TemplateView):
    template_name = 'users/password_reset_complete.html'


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:profile')


class LogoutView(DjangoLogoutView):
    template_name = 'users/logout.html'


class DeleteAccountView(LoginRequiredMixin, View):
    template_name = 'users/delete_account_confirm.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # Удаление аккаунта пользователя
        request.user.delete()

        messages.success(request, 'Ваш аккаунт успешно удален.')
        logout(request)
        return redirect('mailing_service:home')
