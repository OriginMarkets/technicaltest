import datetime
from typing import Any, Dict, List

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from project.bonds.models import Bond, LegalEntity


@pytest.mark.django_db
def test_get_returns_401_if_not_authenticated(client: Any) -> None:
    # Arrange
    url = reverse("bonds:list-view")

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_gets_their_own_bonds(
    django_user_model: Any, client_authed: APIClient, bond_and_legal_entity: Bond
) -> None:
    # Arrange

    # Add a new user and bond
    username = "alsodave"
    password = "Password1!"
    other_user = django_user_model.objects.create(username=username, password=password)
    bnp_paribas = LegalEntity.objects.get(lei="R0MUWSFPU8MPRO8K5P83")
    Bond.objects.create(
        user_id=other_user.id,
        isin="FR0000155501",
        size=50000000,
        currency="EUR",
        maturity=datetime.date(2024, 8, 8),
        legal_entity=bnp_paribas,
    )

    url = reverse("bonds:list-view")
    expected_data = [
        {
            "isin": bond_and_legal_entity.isin,
            "size": bond_and_legal_entity.size,
            "currency": bond_and_legal_entity.currency,
            "maturity": bond_and_legal_entity.maturity.isoformat(),
            "lei": bond_and_legal_entity.legal_entity.lei,
            "legal_name": bond_and_legal_entity.legal_entity.legal_name,
        }
    ]

    # Act
    response = client_authed.get(url)
    actual_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert actual_data == expected_data


@pytest.mark.django_db
def test_filtering_by_lei(
    client_authed: Any, bond_and_legal_entity: Bond, multiple_bonds: List[Bond]
) -> None:
    # Arrange
    url = reverse("bonds:list-view")
    legal_entity = LegalEntity.objects.get(legal_name="DAVE")
    full_url = f"{url}?lei={legal_entity.lei}"
    expected_data = [
        {
            "isin": multiple_bonds[0].isin,
            "size": multiple_bonds[0].size,
            "currency": multiple_bonds[0].currency,
            "maturity": multiple_bonds[0].maturity.isoformat(),
            "lei": multiple_bonds[0].legal_entity.lei,
            "legal_name": multiple_bonds[0].legal_entity.legal_name,
        },
        {
            "isin": multiple_bonds[1].isin,
            "size": multiple_bonds[1].size,
            "currency": multiple_bonds[1].currency,
            "maturity": multiple_bonds[1].maturity.isoformat(),
            "lei": multiple_bonds[1].legal_entity.lei,
            "legal_name": multiple_bonds[1].legal_entity.legal_name,
        },
    ]

    # Act
    response = client_authed.get(full_url)
    actual_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert actual_data == expected_data


@pytest.mark.django_db
def test_filtering_by_bad_lei(
    client_authed: Any, bond_and_legal_entity: Bond, multiple_bonds: List[Bond]
) -> None:
    # Arrange
    url = reverse("bonds:list-view")
    full_url = f"{url}?lei=foo"

    # Act
    response = client_authed.get(full_url)
    actual_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert actual_data == []


@pytest.mark.django_db
def test_filtering_by_legal_name(
    client_authed: Any, bond_and_legal_entity: Bond, multiple_bonds: List[Bond], bond_data: Dict
) -> None:
    # Arrange
    url = reverse("bonds:list-view")
    full_url = f"{url}?legal_name=BNP PARIBAS"
    expected_data = [{**bond_data, "legal_name": "BNP PARIBAS"}]

    # Act
    response = client_authed.get(full_url)
    actual_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert actual_data == expected_data


@pytest.mark.django_db
def test_filtering_by_unmatched_legal_name_returns_empty_dataset(
    client_authed: Any, bond_and_legal_entity: Bond, multiple_bonds: List[Bond], bond_data: Dict
) -> None:
    # Arrange
    url = reverse("bonds:list-view")
    full_url = f"{url}?legal_name=DAVEDAVEDAVE"

    # Act
    response = client_authed.get(full_url)
    actual_data = response.json()

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert actual_data == []
