# users/permissions.py
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User  # Предполагается, что ваша модель пользователя находится в файле users/models.py


def create_dashboard_permissions():
    # Получение типа контента для модели пользователя
    content_type = ContentType.objects.get_for_model(User)

    # Создание разрешения с указанием типа контента
    view_dashboard_permission, created = Permission.objects.get_or_create(
        codename='can_view_dashboard',
        name='Can view dashboard',
        content_type=content_type,
    )
