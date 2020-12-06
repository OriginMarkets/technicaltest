"""This is the pytest file containing fixtures for all the pytest tests"""
import pytest
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token
import uuid

from bonds.factories import BondFactory


register(BondFactory)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_password():
    return 'johnpassword'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def get_or_create_token(db, create_user):
    def get(**kwargs):
        user = create_user()
        token, _ = Token.objects.get_or_create(user=user)
        return user, token
    return get


@pytest.fixture
def api_client_forced_auth(
        db, create_user, api_client
):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
