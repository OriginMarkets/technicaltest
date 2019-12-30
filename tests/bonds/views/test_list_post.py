from typing import Any, Dict

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from project.bonds.models import Bond
from tests.fixtures import API_DATA


@pytest.mark.django_db
def test_api_returns_401_if_not_authenticated(bond_data: Dict) -> None:
    # Arrange
    client = APIClient()

    # Act
    response = client.post("/bonds", bond_data, format="json")

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_can_post_a_bond_with_valid_user(
    responses: Any, client_authed: APIClient, bond_data: Dict
) -> None:
    # Arrange
    lei = bond_data["lei"]
    responses.add(
        "GET", f"{settings.GLIEF_API}?lei={lei}", json=API_DATA, status=status.HTTP_200_OK,
    )

    # Act
    response = client_authed.post("/bonds", bond_data, format="json")

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.json()


def test_cannot_create_duplicate_isin_per_user(
    responses: Any,
    django_user_model: Any,
    client_authed: APIClient,
    bond_and_legal_entity: Bond,
    bond_data: Dict,
) -> None:
    # Arrange
    url = reverse("bonds:list-view")
    expected_error_message = {"non_field_errors": ["isin already exists."]}
    lei = bond_data["lei"]
    responses.add(
        "GET", f"{settings.GLIEF_API}?lei={lei}", json=API_DATA, status=status.HTTP_200_OK,
    )

    # Add a new user and bond
    username = "alsodave"
    password = "Password1!"
    other_user = django_user_model.objects.create(username=username, password=password)

    # Act
    response = client_authed.post(url, bond_data)

    # Auth a different user
    client_alt = APIClient()
    client_alt.force_authenticate(user=other_user)
    response_different_user = client_alt.post(url, bond_data)

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_error_message

    # Constaint doesn't apply to other user
    # This is just so that in the absence of validating isin identifiers
    # a different user can't "work out" other bond IDs.
    assert response_different_user.status_code == status.HTTP_201_CREATED
