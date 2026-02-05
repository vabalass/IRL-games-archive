from django.contrib import admin
from django.utils import timezone
from .models import Game, Category, RecommendedGame
from feedback.models import Comment
from .selectors import recommended_games_anotated_with_avg_rating

class CommentsInLine(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ["author", "text", "rating", "created"]
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

@admin.register(RecommendedGame)
class GameRecommendedAdmin(admin.ModelAdmin):
    list_display = ["environment", "created"]

    def get_queryset(self, request):
        return recommended_games_anotated_with_avg_rating()
    
    def display_avg_rating(self, obj):
        # obj = one RecommendedGame instance. Same as: game = RecommendedGame.objects.get(id=1)
        return obj.avg_rating
    display_avg_rating.short_description = "Avg rating calculated using selectors"

    


