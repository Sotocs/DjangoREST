from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def deactivate_inactive_users():
    threshold = timezone.now() - timedelta(days=30)

    User.objects.filter(
        last_login__lt=threshold,
        is_active=True,
    ).update(is_active=False)
