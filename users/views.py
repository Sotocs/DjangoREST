from users.models import User
from users.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from users.models import Payment
from users.serializers import PaymentSerializer
from rest_framework.response import Response
from rest_framework import status

from users.services.stripe_services import (
    create_stripe_product,
    create_stripe_price,
    create_checkout_session,
)


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = serializer.save(user=request.user)

        if payment.paid_course:
            product_name = payment.paid_course.title
        elif payment.paid_lesson:
            product_name = payment.paid_lesson.title
        else:
            return Response(
                {"detail": "Не указан курс или урок для оплаты."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        product = create_stripe_product(product_name)

        price = create_stripe_price(
            product.id,
            payment.amount,
        )

        session = create_checkout_session(price.id)

        payment.payment_url = session.url
        payment.stripe_session_id = session.id
        payment.save(
            update_fields=[
                "payment_url",
                "stripe_session_id",
            ]
        )

        response_data = self.get_serializer(payment).data

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
        )


class UserViewSet(viewsets.ModelViewSet):
    """CRUD для пользователей — в т.ч. редактирование профиля."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
