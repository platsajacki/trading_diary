import pytest

from rest_framework.test import APIClient

from apps.users.models import User


@pytest.fixture
def user():
    user = User.objects.create_user(username='pytest_user', password='password123')
    return user


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.login(username=user.username, password='password123')
    return client
