# users/utils.py
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def register_confirm(request, user):
    current_site = get_current_site(request)
    context = {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": user.user_token,
    }

    message = f'Поздравляем! ' \
              f'Вы успешно зарегистрированы на Spam Service! ' \
              f'Подтвердите адрес электронной почты, пройдя по ссылке: ' \
              f'http://{current_site}/users/verify_email/{context["uid"]}/{context["token"]}/'
    data = {
        'current_site': current_site,
        'context': context,
        'message': message,
    }
    return data
