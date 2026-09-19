from users.models import User
from users.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "paid_course",
        "paid_lesson",
        "payment_method",
    ]

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]

class UserViewSet(viewsets.ModelViewSet):
    """CRUD для пользователей — в т.ч. редактирование профиля."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
