import factory
from django.utils.text import slugify
from factory.django import DjangoModelFactory

from games_project.feedback.models import Comment
from games_project.games.models import Category
from games_project.games.models import Game
from games_project.games.models import GameWithStats


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    title = factory.Faker("company")
    slug = slugify(title)


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game

    title = factory.Faker("catch_phrase")
    slug = f"{slugify(title)}"
    description = factory.Faker("paragraph")

    category = factory.SubFactory(CategoryFactory)


class GameWithStatsFactory(GameFactory):
    class Meta:
        model = GameWithStats


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    text = factory.Faker("paragraph")
