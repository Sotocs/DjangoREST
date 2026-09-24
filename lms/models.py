from django.db import models


class Course(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Владелец",
    )
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="previews/", null=True, blank=True, verbose_name="Превью"
    )
    description = models.TextField()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Владелец",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
    )
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField()
    preview = models.ImageField(
        upload_to="previews/",
        null=True,
        blank=True,
        verbose_name="Превью",
    )
    video_url = models.URLField(verbose_name="Ссылка на видео")
    link = models.CharField()

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name="Курс",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_course_subscription",
            )
        ]

    def __str__(self):
        return f"{self.user.email} — {self.course.title}"