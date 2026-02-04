from django.contrib import admin
from .models import Game, Category
from feedback.models import Comment

class CommentsInLine(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ["author", "text", "rating", "created"]
    readonly_fields = ["created"]
    ordering = ["created"]
    show_change_link = True

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "description",
        "environment",
        "min_players",
        "max_players",
        "min_duration",
        "max_duration",
        "attachments",
        "equipment_list",
        "category",
        "created",
        "modified",
    )

    prepopulated_fields = {"slug": ("title",)}
    list_display_links = ("title",)
    list_editable = ["environment"]

    inlines = [CommentsInLine]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "created",
        "modified",
    ]

    prepopulated_fields = {"slug": ("title",)}

