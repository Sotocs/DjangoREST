from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    preview = models.ImageField(
        upload_to="previews/", null=True, blank=True, verbose_name="Превью"
    )
    description = models.TextField()

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField()
    preview = models.ImageField(upload_to="previews/", null=True, blank=True, verbose_name="Превью")
    link = models.CharField()

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
