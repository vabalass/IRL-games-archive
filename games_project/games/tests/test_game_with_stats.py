import pytest
from freezegun import freeze_time

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

    def test_last_comment_text_property(self):
        # Arrange
        game_with_stats = GameWithStatsFactory.create()
        user = UserFactory.create()
        CommentFactory.create(game=game_with_stats, author=user)
        CommentFactory.create(game=game_with_stats, author=user)
        # Act
        last_comment = CommentFactory.create(game=game_with_stats, author=user)
        # Assert
        assert last_comment.text == game_with_stats.last_comment_text

    def test_comments_count_last_day_property(self):
        # Arrange
        game_with_stats = GameWithStatsFactory.create()
        user = UserFactory.create()
        # Act
        with freeze_time("2025-01-01"):
            CommentFactory.create(game=game_with_stats, author=user)
            CommentFactory.create(game=game_with_stats, author=user)
            CommentFactory.create(game=game_with_stats, author=user)
        CommentFactory.create(game=game_with_stats, author=user)
        CommentFactory.create(game=game_with_stats, author=user)
        comments_created_today = 2
        # Assert
        assert game_with_stats.comments_count_last_day == comments_created_today

    def test_was_updated_last_day_property(self):
        # Arrange
        with freeze_time("2025-01-01"):
            game_with_stats = GameWithStatsFactory.create()
        # Act
        not_updated = game_with_stats.was_updated_last_day
        game_with_stats.save()
        yes_updated = game_with_stats.was_updated_last_day

        # Assert
        assert not not_updated
        assert yes_updated
