from django.contrib import admin
from django.contrib import messages
from django.contrib.admin import BooleanFieldListFilter, DateFieldListFilter, AllValuesFieldListFilter
from django.utils.translation import ngettext
from feedback.models import Comment
from .models import Game, Category, GameWithStats, Environment
from .selectors import games_anotated_with_stats

class CommentsInLine(admin.TabularInline):
    model = Comment
    extra = 0
    # fieldsets = [
    #     ('None', {
    #         'classes': ['collapse'],
    #         'fields': ["author", "parent", "text", "rating", "created"],
    #     }),
    # ]
    fields = ["author", "parent", "text", "rating", "created"]
    readonly_fields = ["created"]
    classes = ['collapse']
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

@admin.action(description="Set selected games environment to indoor.")
def make_indoor(self, request, queryset):
    updated = queryset.update(environment=Environment.INDOOR)
    self.message_user(
        request,
        ngettext(
            f"%d game was successfuly set as {Environment.INDOOR.label}.",
            f"%d games were successfuly set as {Environment.INDOOR.label}.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )
admin.site.add_action(make_indoor)
        
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
        "comments__author"
    ]

    search_fields = ["title", "description"]

    inlines = [CommentsInLine]

    fieldsets = [
        (
            None,
            {
                "fields": ["title", "slug", "category", "environment", "description",
                            "min_players", "max_players", "min_duration", "max_duration", ],
            },
        ),
        (
            "Advanced options",
            {
                "classes": ["collapse"],
                "fields": ["attachments", "is_active"],
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
class GameStatsAdmin(admin.ModelAdmin):
    list_display = ["title", "average_rating", "display_avg_rating", "display_comment_count", "environment", "created"]

    def get_queryset(self, request):
        return games_anotated_with_stats()
    
    def display_avg_rating(self, obj):
        # obj = one RecommendedGame instance. Same as: game = RecommendedGame.objects.get(id=1)
        return f"{obj.avg_rating:.2f}"

    display_avg_rating.short_description = "Avg rating calculated using selectors"
    display_avg_rating.admin_order_field = "avg_rating"

    def display_comment_count(self, obj):
        return obj.comments_count
    
    display_comment_count.short_description = "Number of comments"

    


