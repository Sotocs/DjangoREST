from django.contrib.auth.models import Group
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LMSTestCase(APITestCase):
    def setUp(self):
        # Обычный пользователь
        self.user = User.objects.create_user(
            email="student1@example.com",
            password="testpassword123",
            username="student1",
        )

        # Второй обычный пользователь
        self.other_user = User.objects.create_user(
            email="student2@example.com",
            password="testpassword123",
            username="student2",
        )

        # Модератор
        self.moderator = User.objects.create_user(
            email="moderator@example.com",
            password="testpassword123",
            username="moderator",
        )

        moderator_group = Group.objects.create(name="Модераторы")
        self.moderator.groups.add(moderator_group)

        # Курс пользователя
        self.course = Course.objects.create(
            title="Тестовый курс",
            description="Описание тестового курса",
            owner=self.user,
        )

        # Урок пользователя
        self.lesson = Lesson.objects.create(
            title="Тестовый урок",
            description="Описание тестового урока",
            video_url="https://www.youtube.com/watch?v=test",
            link="test",
            course=self.course,
            owner=self.user,
        )

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Новый урок",
            "description": "Описание нового урока",
            "video_url": "https://www.youtube.com/watch?v=abc123",
            "link": "test-link",
            "course": self.course.id,
        }

        response = self.client.post("/api/lessons/", data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Новый урок")
        self.assertEqual(response.data["owner"], self.user.id)

    def test_lesson_retrieve(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/lessons/{self.lesson.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.lesson.id)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Изменённый урок",
            "description": self.lesson.description,
            "video_url": self.lesson.video_url,
            "link": self.lesson.link,
            "course": self.course.id,
        }

        response = self.client.put(
            f"/api/lessons/{self.lesson.id}/",
            data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Изменённый урок")

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/api/lessons/{self.lesson.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_other_user_cannot_retrieve_lesson(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(f"/api/lessons/{self.lesson.id}/")

        self.assertEqual(response.status_code, 404)

    def test_other_user_cannot_update_lesson(self):
        self.client.force_authenticate(user=self.other_user)

        data = {
            "title": "Чужой урок",
            "description": self.lesson.description,
            "video_url": self.lesson.video_url,
            "link": self.lesson.link,
            "course": self.course.id,
        }

        response = self.client.put(
            f"/api/lessons/{self.lesson.id}/",
            data,
        )

        self.assertEqual(response.status_code, 404)

    def test_other_user_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(f"/api/lessons/{self.lesson.id}/")

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_moderator_can_retrieve_lesson(self):
        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(f"/api/lessons/{self.lesson.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.lesson.id)

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moderator)

        data = {
            "title": "Урок модератора",
            "description": "Описание",
            "video_url": "https://www.youtube.com/watch?v=abc123",
            "link": "test-link",
            "course": self.course.id,
        }

        response = self.client.post("/api/lessons/", data)

        self.assertEqual(response.status_code, 403)

    def test_moderator_can_update_lesson(self):
        self.client.force_authenticate(user=self.moderator)

        data = {
            "title": "Изменённый модератором урок",
            "description": self.lesson.description,
            "video_url": self.lesson.video_url,
            "link": self.lesson.link,
            "course": self.course.id,
        }

        response = self.client.put(
            f"/api/lessons/{self.lesson.id}/",
            data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["title"],
            "Изменённый модератором урок",
        )

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)

        response = self.client.delete(f"/api/lessons/{self.lesson.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(f"/api/courses/{self.course.id}/subscribe/")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["message"],
            "Вы успешно подписались на курс.",
        )
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course,
            ).exists()
        )

    def test_repeat_subscription(self):
        self.client.force_authenticate(user=self.user)

        Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

        response = self.client.post(f"/api/courses/{self.course.id}/subscribe/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["message"],
            "Вы уже подписаны на этот курс.",
        )
        self.assertEqual(
            Subscription.objects.filter(
                user=self.user,
                course=self.course,
            ).count(),
            1,
        )

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)

        Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

        response = self.client.delete(f"/api/courses/{self.course.id}/subscribe/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["message"],
            "Вы успешно отписались от курса.",
        )
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course,
            ).exists()
        )

    def test_repeat_unsubscribe(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(f"/api/courses/{self.course.id}/subscribe/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data["message"],
            "Вы не подписаны на этот курс.",
        )

    def test_course_is_subscribed(self):
        self.client.force_authenticate(user=self.user)

        Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

        response = self.client.get(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_subscribed"])

    def test_course_is_not_subscribed(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f"/api/courses/{self.course.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.data["is_subscribed"])

    def test_lesson_rejects_non_youtube_url(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "Неверная ссылка",
            "description": "Описание",
            "video_url": "https://rutube.ru/video/test",
            "link": "test-link",
            "course": self.course.id,
        }

        response = self.client.post(
            "/api/lessons/",
            data,
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("video_url", response.data)

    def test_course_pagination(self):
        self.client.force_authenticate(user=self.user)

        Course.objects.create(
            title="Курс 2",
            description="Описание",
            owner=self.user,
        )
        Course.objects.create(
            title="Курс 3",
            description="Описание",
            owner=self.user,
        )

        response = self.client.get("/api/courses/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIsNotNone(response.data["next"])

    def test_lesson_pagination(self):
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            title="Урок 2",
            description="Описание",
            video_url="https://www.youtube.com/watch?v=test2",
            link="test",
            course=self.course,
            owner=self.user,
        )
        Lesson.objects.create(
            title="Урок 3",
            description="Описание",
            video_url="https://www.youtube.com/watch?v=test3",
            link="test",
            course=self.course,
            owner=self.user,
        )

        response = self.client.get("/api/lessons/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 3)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertIsNotNone(response.data["next"])
