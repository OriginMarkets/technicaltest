import pytest
from typing import Any

from project.bonds.models import Bond
from project.bonds.serializers import BondSerializer


@pytest.mark.django_db
def test_ok_bond_data_deserialization(user: Any, bond_and_legal_entity: Bond) -> None:
    # Arrange
    serializer = BondSerializer(instance=bond_and_legal_entity, context={"user_id": user.id})
    expected_data = {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNP PARIBAS",
    }

    # Act
    actual_data = serializer.data

    # Assert
    assert actual_data == expected_data
