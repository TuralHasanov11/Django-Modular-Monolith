from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.identity.models import IdentityUser


class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "is_staff")
    list_filter = ("is_staff",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                )
            },
        ),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    search_fields = ("email", "first_name", "last_name", "username")
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(IdentityUser, UserAdmin)
