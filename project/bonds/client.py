import logging
from typing import Dict, List

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class GliefClientError(Exception):
    pass


class GliefClient:
    def _request(self, method: str, url: str) -> List[Dict]:
        """
        """
        response = requests.request(method, url)
        try:
            response.raise_for_status()
        except requests.HTTPError:
            logger.error("External API call failed - status: %s", response.status_code)
            raise GliefClientError("Failed to fetch data from Glief API") from None
        return response.json()

    def _transform_response(self, raw_data: List[Dict]) -> Dict:
        """
        Convert the Glief API output into a flattened dictionary
        representation for easy parsing.

        :raises: GliefClientError if multiple LEI datasets are found.
        :raises: GliefClientNoDataError if the chosen LEI cannot be found.
        :raises: KeyError is API data is malformed and cannot be parsed.
        """
        lei_data = []
        try:
            for entry in raw_data:
                lei = entry["LEI"]["$"]
                legal_name = entry["Entity"]["LegalName"]["$"]
                lei_data.append({"lei": lei, "legal_name": legal_name})

        except (KeyError, TypeError):
            raise GliefClientError("Failed to convert Glief API Response")

        if len(lei_data) > 1:
            raise GliefClientError("Conflict: Multiple LEI entries found")

        normalized_data = lei_data[0]

        return normalized_data

    def lei_lookup(self, lei: str) -> Dict:
        logger.debug("Converting LEI data - lei: %s", lei)
        url = f"{settings.GLIEF_API}?lei={lei}"
        data = self._request(method="GET", url=url)
        normalised_data = self._transform_response(data)

        return normalised_data
