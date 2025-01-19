from django.contrib import admin

from apps.blog.models import Post
from simple_history.admin import SimpleHistoryAdmin


@admin.register(Post)
class PostAdmin(SimpleHistoryAdmin):
    list_display = (
        "title",
        "updated_by_username",
        "updated_at",
        "is_deleted",
        "deleted_at",
    )
    list_filter = ("title", "is_deleted", "updated_by_username")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "created_at",
                    "created_by_username",
                    "updated_by_username",
                    "updated_at",
                    "is_deleted",
                    "deleted_at",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("title"),
            },
        ),
    )
    readonly_fields = [
        "created_at",
        "created_by_username",
        "updated_by_username",
        "updated_at",
        "is_deleted",
        "deleted_at",
    ]
    # add other fields as readonly
    search_fields = ("title",)
    ordering = ("created_at",)
    filter_horizontal = ()
    history_list_display = ["title"]
    history_list_per_page = 100
