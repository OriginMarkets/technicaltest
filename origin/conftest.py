"""This is the pytest file containing fixtures for all the pytest tests"""
from typing import Any, Callable, Dict, Tuple
import pytest
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.contrib.auth.models import User
import uuid

from bonds.factories import BondFactory


register(BondFactory)


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def test_password():
    return 'johnpassword'


@pytest.fixture
def create_user(db, django_user_model, test_password) -> Callable[[Dict[str, Any]], User]:
    def inner(**kwargs):
        if 'password' not in kwargs:
            kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return inner


@pytest.fixture
def user_and_token(db, create_user) -> Callable[[Dict[str, Any]], Tuple[User, Token]]:
    def inner(**kwargs):
        user = create_user(**kwargs)
        token, _ = Token.objects.get_or_create(user=user)
        return user, token

    return inner


@pytest.fixture
def api_client_forced_auth(
        db, create_user, api_client
) -> APIClient:
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
