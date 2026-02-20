from django.urls import path

from .views import GameDetailsView
from .views import GameListView
from .views import comments_json_view
from .views import reply_view

app_name = "games"

urlpatterns = [
    path("", view=GameListView.as_view(), name="list"),
    path("<slug:slug>/", view=GameDetailsView.as_view(), name="detail"),
    path("<int:game_pk>/comments/", view=comments_json_view, name="comments"),
    path("<int:game_pk>/reply/", view=reply_view, name="reply"),
]
