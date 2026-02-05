from django.db.models import Avg, Q

from .models import RecommendedGame

def recommended_games_that_have_comments_with_rating():
    return RecommendedGame.objects.filter(
        comments__rating__isnull=False, 
        comments__parent__isnull=True
    ).distinct()

def recommended_games_anotated_with_avg_rating():
    # paimti visus games, kiekvienam surasti komentarus, kurie turi reitingą ir neturi tėvų, anotuoti avg_rating stulpelį 
    return recommended_games_that_have_comments_with_rating().annotate(
        avg_rating=Avg('comments__rating')
    )