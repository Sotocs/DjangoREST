from django.urls import path, include
from rest_framework.routers import DefaultRouter

from lms.views import (
    CourseViewSet,
    LessonListCreateView,
    LessonRetrieveUpdateDestroyView,
    CourseSubscriptionView,
)

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list-create"),
    path(
        "lessons/<int:pk>/",
        LessonRetrieveUpdateDestroyView.as_view(),
        name="lesson-detail",
    ),
    path(
        "courses/<int:pk>/subscribe/",
        CourseSubscriptionView.as_view(),
        name="course-subscribe",
    ),
]
