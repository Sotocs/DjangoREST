from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from lms.models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(pk=course_id)

    emails = list(
        Subscription.objects.filter(course=course)
        .values_list("user__email", flat=True)
    )

    if not emails:
        return

    send_mail(
        subject=f"Курс «{course.title}» обновлён",
        message=(
            f"Курс «{course.title}» был обновлён. "
            "Зайдите на платформу, чтобы посмотреть изменения."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=emails,
    )