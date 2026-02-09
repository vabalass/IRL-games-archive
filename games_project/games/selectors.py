from django.db.models import Avg
from django.db.models import Count

from .models import GameWithStats


def games_that_have_comments_with_rating():
    return GameWithStats.objects.filter(
        comments__rating__isnull=False,
    ).distinct()


def games_anotated_with_stats():
    return games_that_have_comments_with_rating().annotate(
        avg_rating=Avg("comments__rating"),
        comments_count=Count("comments", distinct=True),
    )
