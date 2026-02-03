from django.contrib import admin
from .models import Game

# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "environment",
        "min_players",
        "max_players",
        "min_duration",
        "max_duration",
        "attachments",
        "equipment_list",
    )

    list_display_links = ("title",)
    list_editable = ("environment",)

