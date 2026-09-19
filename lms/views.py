from rest_framework import viewsets
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from lms.permissions import IsModerator, IsOwner

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курса через ViewSet."""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Course.objects.all()

        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "destroy":
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ["retrieve", "update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == "create":
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListCreateView(ListCreateAPIView):
    """Список уроков + создание."""

    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated, ~IsModerator]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]

        if course.owner_id != self.request.user.id:
            from rest_framework.exceptions import PermissionDenied

            raise PermissionDenied(
                "Можно создавать уроки только в своих курсах."
            )

        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Получение, обновление и удаление одного урока."""

    serializer_class = LessonSerializer

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)

    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.request.method in ["GET", "PUT", "PATCH"]:
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

