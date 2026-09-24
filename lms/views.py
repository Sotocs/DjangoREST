
from lms.permissions import IsModerator, IsOwner
from lms.paginators import LMSPagination

from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer

from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class CourseViewSet(viewsets.ModelViewSet):
    """CRUD для курса через ViewSet."""

    pagination_class = LMSPagination
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
    pagination_class = LMSPagination
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


class CourseSubscriptionView(APIView):
    """
    Подписка и отписка текущего пользователя от курса.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course,
        )

        if created:
            return Response(
                {"message": "Вы успешно подписались на курс."},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"message": "Вы уже подписаны на этот курс."},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        deleted, _ = Subscription.objects.filter(
            user=request.user,
            course=course,
        ).delete()

        if deleted:
            return Response(
                {"message": "Вы успешно отписались от курса."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Вы не подписаны на этот курс."},
            status=status.HTTP_404_NOT_FOUND,
        )