import json

import pytest

from games_project.games.views import comments_json_view
from games_project.users.tests.factories import UserFactory

from .factories import CommentFactory
from .factories import GameFactory

pytestmark = pytest.mark.django_db  # access to DB


class TestCommentsJsonView:
    def test_comments_json_view_return_correct_comments(self, request_factory):
        # Arrange
        game = GameFactory()
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        rating1 = 5
        rating2 = 9
        comment_count = 2
        # Act
        comment1 = CommentFactory.create(game=game, rating=rating1, author=user1)
        comment2 = CommentFactory.create(game=game, rating=rating2, author=user1)
        reply = CommentFactory.create(
            game=game, rating=9, author=user2, parent=comment2
        )

        request = request_factory.get("/")
        response = comments_json_view(request, game.id)
        data = json.loads(response.content)

        # Assert
        assert isinstance(data, list)
        assert len(data) == comment_count
        assert data[1]["id"] == comment1.id
        assert data[1]["rating"] == rating1
        assert data[0]["id"] == comment2.id
        assert data[0]["rating"] == rating2
        assert data[0]["author_name"] == user1.username
        assert data[0]["replies"][0]["id"] == reply.id
        assert data[0]["replies"][0]["parent_id"] == comment2.id
        assert data[0]["replies"][0]["author_name"] == user2.username
        assert len(data[1]["replies"]) == 0
