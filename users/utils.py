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

    confirmation_link = f'http://{current_site.domain}/users/verify_email/{context["uid"]}/{context["token"]}/'
    message = f'Поздравляем! Вы успешно зарегистрированы! Подтвердите адрес электронной почты, пройдя по ссылке:\n\n{confirmation_link}'

    data = {
        'current_site': current_site,
        'context': context,
        'message': message,
    }
    return data
