import copy
import datetime
from typing import Any, Dict, Iterable, List
from unittest.mock import Mock, patch

import pytest
from rest_framework.test import APIClient

from project.bonds.models import Bond, LegalEntity
from tests.fixtures import API_DATA


@pytest.fixture
def bond_data() -> Dict:
    return {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
    }


@pytest.fixture
def user(django_user_model: Any) -> Any:
    username = "dave"
    password = "Password1!"
    user = django_user_model.objects.create(username=username, password=password)
    return user


@pytest.fixture
def client_authed(user: Any) -> APIClient:
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def bond_and_legal_entity(user: Any) -> Bond:
    legal_entity = LegalEntity.objects.create(legal_name="BNP PARIBAS", lei="R0MUWSFPU8MPRO8K5P83",)
    bond = Bond.objects.create(
        user_id=user.id,
        isin="FR0000131104",
        size=100000000,
        currency="EUR",
        maturity=datetime.date(2025, 2, 28),
        legal_entity=legal_entity,
    )
    return bond


@pytest.fixture
def multiple_bonds(user: Any) -> List[Bond]:
    dave = LegalEntity.objects.create(legal_name="DAVE", lei="D0AVESFIN0ANCE0Z0P00")
    bond_1 = Bond.objects.create(
        user_id=user.id,
        isin="GB0000111111",
        size=400030000,
        currency="EUR",
        maturity=datetime.date(2025, 2, 28),
        legal_entity=dave,
    )
    bond_2 = Bond.objects.create(
        user_id=user.id,
        isin="GB0000111112",
        size=400050000,
        currency="EUR",
        maturity=datetime.date(2028, 3, 31),
        legal_entity=dave,
    )
    return [bond_1, bond_2]


@pytest.fixture
def glief() -> Iterable[Mock]:
    with patch("project.bonds.client.GliefClient._request") as mocked_request:
        mocked_request.return_value = copy.deepcopy(API_DATA)
        yield mocked_request
