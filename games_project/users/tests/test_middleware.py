from datetime import timedelta

import pytest
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from freezegun import freeze_time

from games_project.users.models import UserIp

from .factories import UserFactory

pytestmark = pytest.mark.django_db  # access to DB


class TestUserIpMiddleware:
    def test_non_api_path(self, middleware, request_factory):
        # Arrange
        request = request_factory.get("/about/")
        request.user = UserFactory()
        # Act
        response = middleware.__call__(request)
        # Assert
        assert response is None

    def test_user_ip_saved_once_a_day(self, middleware, request_factory):
        # Arrange
        request = request_factory.get("/about/")
        request.user = UserFactory()
        middleware.__call__(request)
        count_today = UserIp.objects.count()
        # Act
        with freeze_time(timezone.now() + timedelta(days=1, minutes=1)):
            middleware.__call__(request)
            count_tomorrow = UserIp.objects.count()
        with freeze_time(timezone.now() + timedelta(hours=12)):
            middleware.__call__(request)
            count_tomorrow2 = UserIp.objects.count()

        # Assert
        assert count_today + 1 == count_tomorrow == count_tomorrow2

    def test_anonymous_user_ip_not_saved(self, middleware, request_factory):
        # Arrange
        request = request_factory.get("/about/")
        request.user = AnonymousUser()

        # Act
        middleware.__call__(request)

        # Assert
        assert UserIp.objects.count() == 0

    def test_correct_ip_address_saved(self, middleware, request_factory):
        # Arrange
        request = request_factory.get("/about/")
        request.user = UserFactory()

        # Act
        middleware.__call__(request)

        # Assert
        ip = UserIp.objects.filter(user=request.user).latest("created")
        assert ip.ip_address == "127.0.0.1"

    def test_different_users_seperate_ip_records(self, middleware, request_factory):
        # Arrange
        user1 = UserFactory()
        user2 = UserFactory()

        request1 = request_factory.get("/about/")
        request1.user = user1

        request2 = request_factory.get("/about/")
        request2.user = user2
        # Act
        middleware.__call__(request1)
        middleware.__call__(request2)

        # Assert
        user1_count = UserIp.objects.filter(user=user1).count()
        user2_count = UserIp.objects.filter(user=user2).count()

        assert user1_count == 1
        assert user2_count == 1
        assert UserIp.objects.count() == user1_count + user2_count
