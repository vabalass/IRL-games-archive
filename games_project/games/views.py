import json

from django.db.models import F
from django.db.models.functions import TruncDate
from django.http import JsonResponse
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


def comments_json_view(request, game_pk):
    data = list(
        Comment.objects.filter(game__pk=game_pk)
        .annotate(author_name=F("author__username"), date=TruncDate("created"))
        .values()
    )

    return JsonResponse(data, safe=False)


def reply_view(request, game_pk):
    data = json.loads(request.body)
    text = data.get("text", None)

    # Any process that you want
    data = {
        "success": True,
        "message": "It works!",
        "game_pk": game_pk,
        "received_text": text,
    }
    return JsonResponse(data)
