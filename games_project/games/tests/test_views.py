import json

import pytest

from games_project.feedback.models import Comment
from games_project.games.views import comments_json_view
from games_project.games.views import reply_view
from games_project.users.tests.factories import UserFactory

from .factories import CommentFactory
from .factories import GameFactory

pytestmark = pytest.mark.django_db


class TestReplyView:
    def test_reply_view_error_incorrect_field_names(self, request_factory):
        # Arrange
        game = GameFactory()
        user = UserFactory()
        request = request_factory.post(
            "/",
            data=json.dumps({"tt": "bad", "pent": None}),
            content_type="application/json",
        )
        request.user = user

        error_code = 400
        # Act
        response = reply_view(request, game.id)
        data = json.loads(response.content)

        # Assert
        assert response.status_code == error_code
        assert not data["success"]

    def test_reply_view_create_new_comment(self, request_factory):
        # Arrange
        game = GameFactory()
        user = UserFactory()
        comment_text = "very good game"
        request = request_factory.post(
            "/",
            data=json.dumps({"text": comment_text, "parent": None}),
            content_type="application/json",
        )
        request.user = user

        error_code = 200
        # Act
        response = reply_view(request, game.id)
        data = json.loads(response.content)

        # Assert
        assert response.status_code == error_code
        assert data["success"]
        assert data["comment"]["text"] == comment_text
        assert Comment.objects.filter(game=game).exists()

    def test_reply_view_create_reply(self, request_factory):
        # Arrange
        game = GameFactory()
        user = UserFactory()
        parent = CommentFactory(game=game, author=user)
        comment_text = "reply"
        request = request_factory.post(
            "/",
            data=json.dumps({"text": comment_text, "parent": parent.id}),
            content_type="application/json",
        )
        request.user = user
        error_code = 200
        # Act
        response = reply_view(request, game.id)
        data = json.loads(response.content)

        # Assert
        assert response.status_code == error_code
        assert data["success"]
        assert data["comment"]["text"] == comment_text
        assert data["comment"]["parent_id"] == parent.id
        assert Comment.objects.filter(game=game).exists()


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

        response = comments_json_view(request_factory, game.id)
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
