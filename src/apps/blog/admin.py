from django.contrib import admin

from apps.blog.models import Post


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ("title", "updated_by_username", "updated_at", "is_deleted", "delete_at")
    list_filter = ("title", "is_deleted", "updated_by_username")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
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
                    "title",
                ),
            },
        ),
    )
    search_fields = ("title",)
    ordering = ("created_at",)
    filter_horizontal = ()