from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Payment


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ["email"]
    list_display = ("email", "phone_number", "city", "is_staff")
    search_fields = ("email",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payment_date",
        "paid_course",
        "paid_lesson",
        "amount",
        "payment_method",
    )
    list_filter = ("payment_method", "paid_course", "paid_lesson")
    search_fields = ("user__email",)
