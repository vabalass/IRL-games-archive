from django.contrib import admin
from django.utils import timezone
from .models import Game, Category, GameWithStats
from feedback.models import Comment
from .selectors import games_anotated_with_stats

class CommentsInLine(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ["author", "parent", "text", "rating", "created"]
    readonly_fields = ["created"]
    ordering = ["created"]
    show_change_link = True

class GamesInLine(admin.StackedInline):
    model = Game
    extra = 0
    fields = ["title", "min_players", "max_players"]
    readonly_fields = ["title", "min_players", "max_players"]
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

    list_filter = [
        "environment",
        "created",
        "max_duration",
        "equipment",
        "category"
    ]

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
    inlines = [GamesInLine]

@admin.register(GameWithStats)
class GameRecommendedAdmin(admin.ModelAdmin):
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

    


