from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import override_settings
import factory
from rest_framework.test import APITestCase

from bonds.models import Bond


class BondFactory(factory.django.DjangoModelFactory):
    """A test factory for Bond model objects"""

    size = factory.Faker('random_int')
    currency = factory.Faker('currency_code')
    maturity = factory.Faker('future_date')
    # NOTE: If the tests/application were more complex, the isin and lei
    # might need to have the factory generate different values for each
    # bond. But at the current level of simplicity, it's fine to hardcode.
    isin = "FR0000131104"
    lei = "R0MUWSFPU8MPRO8K5P83"

    class Meta:
        model = Bond


class UserFactory(factory.django.DjangoModelFactory):
    """A test factory for User model objects."""
    username = factory.Faker('user_name')

    class Meta:
        model = User


class BondRESTEndpointPermissionTest(APITestCase):
    """Make sure all endpoints require the user to be authenticated"""

    def test_create_requires_authentication(self):
        bond_data = factory.build(dict, FACTORY_CLASS=BondFactory)

        response = self.client.post("/bonds/", bond_data)

        self.assertEqual(response.status_code, 403)

    def test_list_requires_authentication(self):
        response = self.client.get("/bonds/")

        self.assertEqual(response.status_code, 403)


class BondCreateAPITest(APITestCase):
    """Test the create REST view"""

    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

    @patch('bonds.serializers.requests.get')
    def test_bond_create_view(self, mocked_get):
        mocked_gleif_json = [{'Entity': {'LegalName': {'$': 'BNPPARIBAS'}}}]
        mocked_get.return_value = Mock(json=lambda: mocked_gleif_json)
        bond_data = factory.build(dict, FACTORY_CLASS=BondFactory)

        response = self.client.post("/bonds/", bond_data)

        # First check the REST API response is correct
        self.assertEqual(response.status_code, 201)
        expected_json = {
            "isin": bond_data['isin'],
            "size": bond_data['size'],
            "currency": bond_data['currency'],
            "maturity": str(bond_data['maturity']),
            "lei": bond_data['lei'],
            "legal_name": "BNPPARIBAS",  # fetched from GLEIF API
        }
        self.assertDictEqual(response.json(), expected_json)
        # Now check the bond object was correctly created in the db
        created_bond = Bond.objects.get()  # will raise an exception if more than one bond created
        self.assertEqual(created_bond.isin, bond_data['isin'])
        self.assertEqual(created_bond.size, bond_data['size'])
        self.assertEqual(created_bond.currency, bond_data['currency'])
        self.assertEqual(created_bond.maturity, bond_data['maturity'])
        self.assertEqual(created_bond.lei, bond_data['lei'])
        self.assertEqual(created_bond.legal_name, "BNPPARIBAS")
        # The current user should be saved so as to determine which user
        # has permission to view the bond
        self.assertEqual(created_bond.user, self.user)
        # And check the GLEIF API was correctly called to retrieve the legal name
        expected_url = 'https://leilookup.gleif.org/api/v2/leirecords?lei=' + bond_data['lei']
        mocked_get.assert_called_with(expected_url)

    @override_settings(GLEIF_URL='http://some-other-url.com')
    @patch('bonds.serializers.requests.get')
    def test_gleif_url_taken_from_settings(self, mocked_get):
        mocked_gleif_json = [{'Entity': {'LegalName': {'$': 'BNPPARIBAS'}}}]
        mocked_get.return_value = Mock(json=lambda: mocked_gleif_json)
        bond_data = factory.build(dict, FACTORY_CLASS=BondFactory)

        self.client.post("/bonds/", bond_data)

        # Check the url used to get the legal name is taken from the
        # GLEIF_URL setting rather than hardcoded
        expected_url = 'http://some-other-url.com?lei=' + bond_data['lei']
        mocked_get.assert_called_with(expected_url)


class BondListAPITest(APITestCase):
    """Test the list REST view"""

    def setUp(self):
        self.user = UserFactory()
        self.client.force_login(self.user)

    def test_bond_list_view(self):
        bond1 = BondFactory(legal_name="BNPPARIBAS", user=self.user)
        bond2 = BondFactory(legal_name="BARCLAYS", user=self.user)

        response = self.client.get("/bonds/")

        self.assertEqual(response.status_code, 200)
        expected_json = [
            {
                "isin": bond1.isin,
                "size": bond1.size,
                "currency": bond1.currency,
                "maturity": str(bond1.maturity),
                "lei": bond1.lei,
                "legal_name": "BNPPARIBAS",
            },
            {
                "isin": bond2.isin,
                "size": bond2.size,
                "currency": bond2.currency,
                "maturity": str(bond2.maturity),
                "lei": bond2.lei,
                "legal_name": "BARCLAYS",
            },
        ]
        self.assertListEqual(response.json(), expected_json)

    def test_bond_list_view_filters_by_legal_name(self):
        BondFactory(legal_name='BARCLAYS', user=self.user)
        bond = BondFactory(legal_name='HALIFAX', user=self.user)

        response = self.client.get("/bonds/?legal_name=HALIFAX")

        self.assertEqual(response.status_code, 200)
        expected_json = [
            {
                "isin": bond.isin,
                "size": bond.size,
                "currency": bond.currency,
                "maturity": str(bond.maturity),
                "lei": bond.lei,
                "legal_name": "HALIFAX",
            },
        ]
        self.assertListEqual(response.json(), expected_json)

    def test_bond_list_view_displays_only_users_own_bonds(self):
        user2 = UserFactory()
        bond = BondFactory(legal_name="BNPPARIBAS", user=self.user)
        BondFactory(legal_name="BARCLAYS", user=user2)

        response = self.client.get("/bonds/")

        self.assertEqual(response.status_code, 200)
        expected_json = [
            {
                "isin": bond.isin,
                "size": bond.size,
                "currency": bond.currency,
                "maturity": str(bond.maturity),
                "lei": bond.lei,
                "legal_name": "BNPPARIBAS",
            },
        ]
        self.assertListEqual(response.json(), expected_json)
