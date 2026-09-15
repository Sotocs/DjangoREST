from rest_framework import serializers

from users.models import User
from users.models import Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "phone_number", "city", "avatar"]
        read_only_fields = ["id", "email"]

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"