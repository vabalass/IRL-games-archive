import pytest
from django.core.cache import cache
from django.test import RequestFactory
from users.middleware import UserIpMiddleware

from .factories import UserFactory


class TestUserIpMiddleware:
    @pytest.fixture
    def middleware(self):
        return UserIpMiddleware(
            get_response=lambda r: None
        )  # None so it doesnt call next middleware

    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    @pytest.fixture
    def clear_cache(self):
        cache.clear()
        yield
        cache.clear()

    def test_non_api_path(self, middleware, request_factory):
        # Arrange
        request = self.request_factory.get("/about/")
        request.user = UserFactory()
        # Act
        response = middleware.__call__(request)
        # Assert
        assert response is None
