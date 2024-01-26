from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User,
    Experience
)
admin.site.register(Experience)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "is_active",
        "is_trainer",
        "created_at",
    )
    list_filter = ("is_active",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email", "state", "city", "latitude", "longitude")}),
        (
            ("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_trainer"),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "username",
                    "first_name",
                    "last_name",
                    "state", 
                    "city", 
                    "latitude", 
                    "longitude",
                    "is_active",
                    "is_staff", 
                    "is_trainer", 
                ),
            },
        ),
    )
