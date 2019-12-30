from typing import Any

import pytest
from rest_framework import status

from project.bonds.client import GliefClient, GliefClientError
from tests.fixtures import API_DATA


@pytest.mark.parametrize("error_code", [400, 401, 402, 500, 502, 503])
def test_client_request_raising_error_converted_to_client_error(
    responses: Any, error_code: int
) -> None:
    # Arrange
    lei = "123456789012345"
    client = GliefClient()
    responses.add(
        "GET", f"https://leilookup.gleif.org/api/v2/leirecords?lei={lei}", status=error_code
    )

    # Act
    # Assert
    with pytest.raises(GliefClientError):
        client.lei_lookup(lei)


def test_client_request_with_ok_response(responses: Any) -> None:
    # Arrange
    lei = "123456789012345"
    client = GliefClient()
    responses.add(
        "GET",
        f"https://leilookup.gleif.org/api/v2/leirecords?lei={lei}",
        json=API_DATA,
        status=status.HTTP_200_OK,
    )

    # Act
    lei_data = client.lei_lookup(lei)

    # Assert
    assert isinstance(lei_data, dict)


def test_malformed_data_response_raises_correct_exception() -> None:
    # Arrange
    client = GliefClient()

    # Act
    with pytest.raises(GliefClientError) as excinfo:
        client._transform_response("<Bad Response 400>")

    # Assert
    assert "Failed to convert Glief API Response" in str(excinfo.value)


def test_client_raises_if_multiple_lei_datasets_found() -> None:
    # Arrange
    client = GliefClient()
    duplicated_datasets = [API_DATA[0], API_DATA[0]]

    # Act
    with pytest.raises(GliefClientError) as excinfo:
        client._transform_response(duplicated_datasets)

    # Assert
    assert "Conflict: Multiple LEI entries found" in str(excinfo.value)


def test_client_coverts_api_response_to_flatten_data_structure() -> None:
    # Arrange
    client = GliefClient()
    expected_normalized_data = {
        "lei": "R0MUWSFPU8MPRO8K5P83",
        "legal_name": "BNP PARIBAS",
    }

    # Act
    actual_normalised_data = client._transform_response(API_DATA)

    # Assert
    assert actual_normalised_data == expected_normalized_data
