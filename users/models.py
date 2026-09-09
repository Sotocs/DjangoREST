from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Email адрес")

    phone_number = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="Номер телефона"
    )
    city = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Страна"
    )
    avatar = models.ImageField(
        upload_to="avatars/", null=True, blank=True, verbose_name="Аватар"
    )

    # Указываем, что для авторизации используется email
    USERNAME_FIELD = "email"
    # Поля, которые будут запрашиваться при создании суперпользователя (кроме пароля)
    REQUIRED_FIELDS = []

    # objects = UserManager()
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
