from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import validate_youtube_url

class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(
        validators=[validate_youtube_url]
    )

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ["owner"]


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ["owner"]

    def get_count_lessons(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return False

        return obj.subscriptions.filter(
            user=request.user
        ).exists()

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["id", "user", "course"]
        read_only_fields = ["id", "user"]