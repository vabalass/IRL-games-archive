import json

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView
from django.views.generic import ListView

from games_project.feedback.models import Comment

from .forms import CommentForm
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
    data = Comment.get_all_for_game(game_pk)

    return JsonResponse(data, safe=False)


@login_required
@require_http_methods(["POST"])
def reply_view(request, game_pk):
    try:
        data = json.loads(request.body)
        form = CommentForm(data)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.game_id = game_pk
            comment.author = request.user
            comment.parent = form.cleaned_data.get("parent")
            comment.save()

            return JsonResponse({"success": True, "comment": comment.to_dict()})
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    except (json.JSONDecodeError, ValidationError) as e:
        return JsonResponse(
            {"success": False, "errors": {"general": str(e)}}, status=400
        )
