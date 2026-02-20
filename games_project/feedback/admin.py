from django.contrib import admin

from .models import Comment


# Register your models here.
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "game",
        "parent",
        "text",
        "rating",
        "upvotes",
        "downvotes",
        "attachment",
    ]

    list_display_links = ["text"]
    list_editable = ["rating", "upvotes", "downvotes"]
    ordering = ["-created"]
