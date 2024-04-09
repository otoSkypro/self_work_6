# users/signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .permissions import create_dashboard_permissions


@receiver(post_migrate)
def create_permissions(sender, **kwargs):
    create_dashboard_permissions()
