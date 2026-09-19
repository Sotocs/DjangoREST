from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ["owner"]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор курса с подсчётом уроков и выводом самих уроков."""

    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["owner"]

    def get_count_lessons(self, obj):
        return obj.lessons.count()
