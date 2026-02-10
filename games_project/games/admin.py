from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import BooleanFieldListFilter
from django.contrib.admin import DateFieldListFilter

from games_project.feedback.models import Comment

from .decorators import remove_delete_actions
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


class GroupSizeListFilter(admin.SimpleListFilter):
    title = "Players group size"
    parameter_name = "group_size"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Under 10"),
            ("10-20", "Between 10 and 20"),
            ("21-50", "Between 21 and 50"),
            ("50+", "Between 50+"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(
                max_players__lt=10,
            )
        if self.value() == "10-20":
            return queryset.filter(
                max_players__lt=21,
            )
        if self.value() == "21-50":
            return queryset.filter(
                max_players__lt=51,
            )
        if self.value() == "50+":
            return queryset.filter(
                max_players__gt=50,
            )

        return None


@admin.action(description="Set selected games environment to indoor")
def make_indoor(self, request, queryset):
    updated = queryset.update(environment=Environment.INDOOR)
    message = f"{updated} game(s) were successfully set as {self.environment_label}"

    self.message_user(request, message, messages.SUCCESS)


@admin.action(description="Soft delete selected games")
def soft_delete(self, request, queryset):
    updated = queryset.update(is_active=False)
    message = f"{updated} game(s) were successfully soft_deleted"

    self.message_user(request, message, messages.SUCCESS)


admin.site.add_action(make_indoor)
admin.site.add_action(soft_delete)


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

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def has_delete_permission(self, request, obj=None):
        return False


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
        "last_24h_comments_count",
        "display_updated_in_last_24_hours",
        "is_active",
        "average_rating",
        "display_avg_rating",
        "display_comment_count",
        "environment",
        "created",
    ]

    def get_queryset(self, request):
        return games_anotated_with_stats()

    @admin.display(
        description="Avg rating calculated using selectors",
        ordering="avg_rating",
    )
    def display_avg_rating(self, obj):
        # obj = one RecommendedGame instance.
        return f"{obj.avg_rating:.2f}"

    @admin.display(description="Number of comments")
    def display_comment_count(self, obj):
        return obj.comments_count

    @admin.display(description="Updated in last 24h", boolean=True)
    def display_updated_in_last_24_hours(self, obj):
        return obj.has_been_updated_in_last_24_hours
