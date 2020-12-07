import pytest
from django.urls import reverse
from rest_framework import status
from bonds.models import Bond


@pytest.mark.django_db
def test_root(api_client_forced_auth):
    resp = api_client_forced_auth.get("/")
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_unauthorized_user(api_client):
    resp = api_client.get("/")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_bonds(api_client, get_or_create_token, bond_factory):
    url = reverse('bonds')
    user, token = get_or_create_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    bond = bond_factory(user=user)

    resp = api_client.get(url)

    assert resp.status_code == status.HTTP_200_OK
    resp_bond = resp.json()[0]
    assert resp_bond['isin'] == bond.isin
    assert resp_bond['size'] == bond.size
    assert resp_bond['currency'] == bond.currency
    assert resp_bond['maturity'] == bond.maturity.strftime('%Y-%m-%d')
    assert resp_bond['lei'] == bond.lei
    assert resp_bond['legal_name'] == bond.legal_name


@pytest.mark.django_db
def test_list_bonds_by_legal_name(api_client, get_or_create_token, bond_factory):
    url = reverse('bonds')
    user, token = get_or_create_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    bond = bond_factory(user=user)

    resp = api_client.get(url, data={'legal_name': bond.legal_name})

    assert resp.status_code == status.HTTP_200_OK
    resp_bond = resp.json()[0]
    assert resp_bond['isin'] == bond.isin
    assert resp_bond['size'] == bond.size
    assert resp_bond['currency'] == bond.currency
    assert resp_bond['maturity'] == bond.maturity.strftime('%Y-%m-%d')
    assert resp_bond['lei'] == bond.lei
    assert resp_bond['legal_name'] == bond.legal_name


@pytest.mark.django_db
def test_list_bonds_user_isolation(api_client, get_or_create_token, bond_factory):
    url = reverse('bonds')
    user_logged_in, token = get_or_create_token()
    user2, _ = get_or_create_token()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    bond = bond_factory(user=user_logged_in, lei='21380016UZS36PC85Y22')
    bond2 = bond_factory(user=user_logged_in, lei='21380016UZS36PC85Y22')
    bond_not_to_be_listed = bond_factory(user=user2, lei='894500TFYBOUIM1WUN34')

    resp = api_client.get(url)

    assert resp.status_code == status.HTTP_200_OK
    bonds = resp.json()
    assert len(bonds) == 2
    assert bonds[0]['lei'] != bond_not_to_be_listed.lei
    assert bonds[1]['lei'] != bond_not_to_be_listed.lei
    assert bond.isin in [b['isin'] for b in bonds]
    assert bond2.isin in [b['isin'] for b in bonds]


@pytest.mark.django_db
def test_create_bond(db, api_client_forced_auth):
    url = reverse('bonds')
    data = {
        "isin": "FR0000131104",
        "size": 100000000,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83"
    }

    resp = api_client_forced_auth.post(url, data=data)
    bond = Bond.objects.first()

    assert resp.status_code == status.HTTP_201_CREATED
    assert bond.isin == data['isin']
    assert bond.size == data['size']
    assert bond.currency == data['currency']
    assert bond.maturity.strftime('%Y-%m-%d') == data['maturity']
    assert bond.lei == data['lei']
    assert bond.legal_name == 'BNP PARIBAS'
