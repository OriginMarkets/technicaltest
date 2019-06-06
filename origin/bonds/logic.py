import json
import logging
import requests
from django.conf import settings


LOG = logging.getLogger(__name__)


def fetch_legal_entities_names(leis, timeout=5):
    """
    Simple wrapper to fetch entities names from third party API.

    Args:
        leis (list): list of Legal Entity Identifiers
        timeout (int): Timeout to be set on request, in seconds.

    Returns:
        dict: map of leis and legal names
            {lei: legal_name}
    """

    resp = None

    try:
        resp = requests.get(settings.LEI_LOOKUP_URL, params={'lei': leis}, timeout=timeout)
    except (requests.ConnectionError, requests.Timeout) as e:
        # in such case we could have some retry strategy to try to wait for the service or network to come back to life
        LOG.warning('Could not get response from GLEIF LEI Look-up API for leis %s.', leis, exc_info=e)
    except requests.RequestException:
        LOG.exception('Request to GLEIF LEI Look-up API failed miserably for leis %s.', leis)

    if not resp:
        return None

    if resp.status_code != 200:
        # in case fo 5xx we could also go into retry flow, for the rest we should very likely take swift action, so error level
        LOG.error('Got a %s response from GLEIF LEI Look-up API.', resp.status_code)
        return None

    try:
        return {
            entry['LEI']['$']: entry['Entity']['LegalName']['$']
            for entry in json.loads(resp.content)
        }
    except (json.decoder.JSONDecodeError, KeyError):
        LOG.exception('Unsupported response format from GLEIF LEI Look-up API.')

    return None


def fetch_legal_entity_name(lei, timeout=5):
    """
    Simple wrapper to fetch entity name from third party API.

    Args:
        lei (str): Legal Entity Identifier
        timeout (int): Timeout to be set on request, in seconds.

    Returns:
        str: Legal Entity name
    """

    lei_name_map = fetch_legal_entities_names([lei], timeout)

    if lei_name_map:
        return lei_name_map.get(lei)

    return None
