import pytest
from django.test import RequestFactory

from games_project.users.middleware import UserIpMiddleware
from games_project.users.models import User
from games_project.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def middleware():
    return UserIpMiddleware(
        get_response=lambda r: None
    )  # None so it doesnt call next middleware
