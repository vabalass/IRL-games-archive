import pytest

from games_project.users.tests.factories import UserFactory

from .factories import CommentFactory
from .factories import GameWithStatsFactory

pytestmark = pytest.mark.django_db  # access to DB


class TestGameWithStats:
    def test_average_rating_calculation_correct(self):
        # Arrange
        game_with_stats = GameWithStatsFactory.create()
        user = UserFactory.create()
        CommentFactory.create(game=game_with_stats, rating=5, author=user)
        CommentFactory.create(game=game_with_stats, rating=9, author=user)
        # Act
        average_rating_property = game_with_stats.average_rating
        # Assert
        assert average_rating_property == "7.00"
