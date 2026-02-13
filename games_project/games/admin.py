from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import BooleanFieldListFilter
from django.contrib.admin import DateFieldListFilter

from games_project.feedback.models import Comment

from .decorators import remove_delete_actions
from .decorators import title
from .models import Category
from .models import Environment
from .models import Game
from .models import GameWithStats
from .selectors import games_anotated_with_stats


class CommentsInLine(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ["author", "parent", "text", "rating", "created"]
    readonly_fields = ["created"]
    classes = ["collapse"]
    ordering = ["created"]
    show_change_link = True


class GamesInLine(admin.StackedInline):
    model = Game
    extra = 0
    fields = ["title", "min_players", "max_players"]
    readonly_fields = ["title", "min_players", "max_players"]
    ordering = ["created"]
    show_change_link = True


@title("Players group size")
class GroupSizeListFilter(admin.SimpleListFilter):
    parameter_name = "group_size"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Under 10"),
            ("10-20", "Between 10 and 20"),
            ("21-50", "Between 21 and 50"),
            ("50+", "Above 50"),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        match value:
            case "<10":
                return queryset.filter(min_players__lt=10)
            case "10-20":
                return queryset.filter(
                    max_players__gte=10,
                    min_players__lte=20,
                )
            case "21-50":
                return queryset.filter(
                    max_players__gte=21,
                    min_players__lte=50,
                )
            case "50+":
                return queryset.filter(max_players__gte=50)
            case _:
                return queryset


@admin.action(description="Set selected games environment to indoor")
def make_indoor(self, request, queryset):
    updated = queryset.update(environment=Environment.INDOOR)
    message = f"{updated} game(s) were successfully set as {Environment.INDOOR.label}"

    self.message_user(request, message, messages.SUCCESS)


@admin.action(description="Reset games rating (comments rating will be set to None)")
def reset_rating(self, request, queryset):
    updated = Comment.objects.filter(game__in=queryset).update(rating=None)

    message = f"{updated} comment ratings(s) were successfully reset"
    self.message_user(request, message, messages.SUCCESS)


@admin.action(description="Soft delete selected games")
def soft_delete(self, request, queryset):
    updated = queryset.update(is_active=False)
    message = f"{updated} game(s) were successfully soft_deleted"

    self.message_user(request, message, messages.SUCCESS)


class NoDeleteMixin:
    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Game)
class GameAdmin(NoDeleteMixin, admin.ModelAdmin):
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
    actions = [reset_rating, soft_delete, make_indoor]

    list_filter = [
        GroupSizeListFilter,
        ("is_active", BooleanFieldListFilter),
        "environment",
        ("created", DateFieldListFilter),
        "max_duration",
        "equipment",
        "category",
        "comments__author",
    ]

    search_fields = ["title", "description"]

    inlines = [CommentsInLine]

    fieldsets = [
        (
            None,
            {
                "fields": [
                    "title",
                    "slug",
                    "category",
                    "environment",
                    "description",
                    "min_players",
                    "max_players",
                    "min_duration",
                    "max_duration",
                    "is_active",
                ],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["attachments"],
            },
        ),
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "slug",
        "created",
        "modified",
    ]

    prepopulated_fields = {"slug": ("title",)}
    inlines = [GamesInLine]


@admin.register(GameWithStats)
@remove_delete_actions
class GameStatsAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "last_comment",
        "comments_count_last_day",
        "display_updated_last_day",
        "is_active",
        "average_rating",
        "display_avg_rating",
        "display_comment_count",
        "environment",
        "created",
    ]

    actions = [reset_rating, soft_delete]

    def get_queryset(self, request):
        return games_anotated_with_stats()

    @admin.display(ordering="avg_rating")
    @title("Avg rating calculated using selectors")
    def display_avg_rating(self, obj):
        return f"{obj.avg_rating:.2f}"

    @admin.display(description="Number of comments")
    def display_comment_count(self, obj):
        return obj.comments_count

    @admin.display(description="Updated last day", boolean=True)
    def display_updated_last_day(self, obj):
        return obj.was_updated_last_day
