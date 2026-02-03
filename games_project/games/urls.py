from django.urls import path
from .views import GameDetailsView, GameListView

app_name = 'games'

urlpatterns = [
    path('', view=GameListView.as_view(), name="list"),
    path('<int:pk>/', view=GameDetailsView.as_view(), name="detail")
]
