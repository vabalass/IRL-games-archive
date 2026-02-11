from django.views.generic import DetailView
from django.views.generic import ListView

from games_project.feedback.models import Comment

from .models import Game


class GameListView(ListView):
    model = Game
    context_object_name = "games"
    template_name = "games/list.html"


class GameDetailsView(DetailView):
    model = Game
    template_name = "games/detail.html"
    context_object_name = "game"


class CommentsView(ListView):
    model = Comment
    template_name = "games/comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(game__pk=self.kwargs["pk"])
