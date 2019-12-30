from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_health_works_without_authentication(client: Any) -> None:
    # Arrange

    # Act
    response = client.get(reverse("health"))

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
