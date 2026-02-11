from django.urls import path

from .views import CommentsView
from .views import GameDetailsView
from .views import GameListView

app_name = "games"

urlpatterns = [
    path("", view=GameListView.as_view(), name="list"),
    path("<slug:slug>/", view=GameDetailsView.as_view(), name="detail"),
    path("<int:pk>/comments/", view=CommentsView.as_view(), name="comments"),
]
