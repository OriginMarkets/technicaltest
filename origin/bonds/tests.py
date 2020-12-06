import pytest
from rest_framework import status


@pytest.mark.django_db
def test_root(api_client_auth):
    resp = api_client_auth.get("/")
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_user(api_client):
    resp = api_client.get("/")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
