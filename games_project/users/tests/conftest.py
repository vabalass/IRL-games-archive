import pytest
from django.test import RequestFactory

from games_project.users.middleware import UserIpMiddleware


@pytest.fixture
def middleware(self):
    return UserIpMiddleware(
        get_response=lambda r: None
    )  # None so it doesnt call next middleware


@pytest.fixture
def request_factory(self):
    return RequestFactory()
