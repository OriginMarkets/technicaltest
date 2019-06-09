from rest_framework.test import APITestCase
from django.urls import reverse
from bonds.models import Bond
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from functools import partial

# Just for hinting
User = get_user_model()


class BondsTest(APITestCase):
    """
    This tests all of the avilable methods/endpoints with different body structures
    checking for corner cases for specific responses
    """

    # A list of available endpoints, use partial for reverses with arguments
    URL_POST = reverse('bonds-lp')
    URL_LIST = reverse('bonds-lp')
    URL_GET = partial(reverse, 'bonds-gud')
    URL_PUT = partial(reverse, 'bonds-gud')
    URL_DELETE = partial(reverse, 'bonds-gud')

    # tokens application must be enabled in settings.py
    LOGIN_URL = reverse('token-login')

    # Our set of available users, 2 to test segregation
    USERA = "gates"
    USERB = "jobs"
    PASSA = "windowsseven"
    PASSB = "applemacbook"

    @classmethod
    def setUpTestData(cls):
        """
        We need to setup the Users and create the tokens if not there already
        """
        User = get_user_model()
        jobs = User.objects.create_user(username=cls.USERB, password=cls.PASSB)
        gates = User.objects.create_user(username=cls.USERA, password=cls.PASSA)
        Token.objects.create(user=jobs)
        Token.objects.create(user=gates)

    # List of different bonds, valid and invalid
    # Valid bond A
    VALID_BONDA = {
        "isin": "FR0000111204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "R0MUWSFPU8MPRO8K5P83"
    }
    # Valid bond A legal_name *must match the GLEIF result!
    VALID_BONDA_LEGAL_NAME = "BNP PARIBAS"

    # Valid bond B
    VALID_BONDB = {
        "isin": "FR0000112204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "029200067A7K6CH0H586",
    }
    # Valid bond B legal_name *must match the GLEIF result!
    VALID_BONDB_LEGAL_NAME = "CENTRAL SECURITIES CLEARING SYSTEM PLC"

    # We must not be able to update or post the key 'legal_name' as it is fetched
    INVALID_LEGAL_NAME_KEY_BOND = {
        "isin": "FR0000112204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "029200067A7K6CH0H586",
        "legal_name": "FooBar PLC"
    }

    # This LEI does not exists on the GLEIF API when searched at the time of writing,
    # though the format is correct!
    INEXISTENT_LEI_BOND = {
        "isin": "FR0000112204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "029200068A7K6CH0H586",
    }

    # Invalid lei format, too short
    INVALID_LEN_LEI_BOND = {
        "isin": "FR0000112204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "02920006",
    }

    # Invalid lei format, not alphanumeric, too long
    INVALID_FORMAT_LEI_BOND = {
        "isin": "FR0000112204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "YWRmYWRmYXNmZGFzZmFkZmFzZgo=",
    }

    # Invalid maturity date
    INVALID_FORMAT_MATURITY_BOND = {
        "isin": "FR0000112204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28T",
        "lei": "029200067A7K6CH0H586",
    }

    # Invalid currency *outside iso standards!
    INVALID_CURRENCY_BOND = {
        "isin": "FR0000112204",
        "size": 10,
        "currency": "BTC",
        "maturity": "2025-02-28",
        "lei": "029200067A7K6CH0H586",
    }

    # Negative sizes should not be allowed, though zero size may represent something
    INVALID_SIZE_BOND = {
        "isin": "FR0000112204",
        "size": -10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "029200067A7K6CH0H586",
    }

    # Invalid ISIN format, must have two letters at the beggining
    INVALID_ISIN_BOND = {
        "isin": "100000112204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "lei": "029200067A7K6CH0H586",
    }

    # Invalid key "gleif", human error
    INVALID_KEY_BOND = {
        "isin": "100000112204",
        "size": 10,
        "currency": "EUR",
        "maturity": "2025-02-28",
        "gleif": "029200067A7K6CH0H586",
    }

    def test_forbidden(self):
        """
        We should not be able to fetch anything if not logged in
        """
        resp = self.client.get(self.URL_LIST)
        assert resp.status_code == 403

    def _add_bond_model(self, bond: dict, username: User) -> Bond:
        """
        Helper function that adds a model using the backend

        :param bond: A dictionary representing a bond
        :param username: An instance of get_user_model() to pass to the constructor

        :returns: An instance of a saved Bond
        """
        User = get_user_model()
        user = User.objects.get(username=username)
        bond = Bond(**bond, user=user)
        bond.save()
        return bond

    def _delete_all_bonds(self):
        """
        Helper function to delete all the Bonds
        Used to substitute the setUp of unit.test.TestCase which I couldn't find
        on the documentation of rest_framework
        """
        Bond.objects.all().delete()

    def _login(self, user: str, pasw: str) -> dict:
        """
        Helper function to login against the token application and setup the
        credentials for subsequent calls

        :param user: username for logging in
        :param pasw: password for specified user

        :returns: A token used for authentication
        """
        resp = self.client.post(
            self.LOGIN_URL,
            {'username': user, 'password': pasw},
            format="json"
        )
        token = resp.data.get('token', None)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        return token

    def test_login(self):
        """
        Tests login functionality
        """
        token = self._login(self.USERA, self.PASSA)
        self.assertNotEqual(token, None, msg="Login does not work, missing test user?")
        token = self._login(self.USERB, self.PASSB)
        self.assertNotEqual(token, None, msg="Login does not work, missing test user?")

    def test_empty_list(self):
        """
        If nothing is in the backend the reponse is an empty list
        """
        self._login(self.USERA, self.PASSA)
        Bond.objects.all().delete()
        resp = self.client.get(self.URL_LIST)
        self.assertEqual(resp.data, [])

    def test_not_empty_list(self):
        """
        A populated backend must show a list of bonds, in this case the length is 1
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_LIST)
        self.assertEqual(len(resp.data), 1, msg="The list returned more than one bond")
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data[0])

    def test_legal_name_filter(self):
        """
        Test filtering of legal_names
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        self._add_bond_model(self.VALID_BONDB, self.USERA)
        resp = self.client.get(self.URL_LIST)
        self.assertEqual(len(resp.data), 2, msg="The list returned only one bond")
        resp = self.client.get(self.URL_LIST, data={'legal_name': self.VALID_BONDA_LEGAL_NAME})
        self.assertEqual(len(resp.data), 1, msg="The list returned only one bond")
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data[0])

    def test_user_segregation(self):
        """
        Each user must be able to list only it's own bonds
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        respa = self.client.get(self.URL_LIST)
        self.assertEqual(len(respa.data), 1, msg="The list returned more than one bond")
        self.assertDictContainsSubset(self.VALID_BONDA, respa.data[0])
        self._login(self.USERB, self.PASSB)
        self._add_bond_model(self.VALID_BONDB, self.USERB)
        respb = self.client.get(self.URL_LIST)
        self.assertEqual(len(respb.data), 1, msg="The list returned more than one bond")
        self.assertDictContainsSubset(self.VALID_BONDB, respb.data[0])
        self.assertNotEqual(respa.data[0], respb.data[0])

    def test_post(self):
        """
        Test posting a bond
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.VALID_BONDA, format="json")
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)

    def test_invalid_key_post(self):
        """
        Test invalid key posting
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INVALID_KEY_BOND, format="json")
        self.assertEquals(resp.status_code, 400)

    def test_invalid_legal_name_post(self):
        """
        Test invalid legal_name posting
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INVALID_LEGAL_NAME_KEY_BOND, format="json")
        self.assertEquals(resp.status_code, 400)

    def test_known_legal_name_of_lei(self):
        """
        Test that the fetching from the GLEIF API works
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.VALID_BONDA, format="json")
        full_valid_bonda = {
            **{'legal_name': self.VALID_BONDA_LEGAL_NAME},
            **self.VALID_BONDA
        }
        self.assertDictEqual(full_valid_bonda, resp.data)

    def test_inexistent_lei_post(self):
        """
        Test that we cover an inxesintent LEI
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INEXISTENT_LEI_BOND, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_len_lei_post(self):
        """
        Test that we cover an invalid length LEI
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INVALID_LEN_LEI_BOND, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_format_lei_post(self):
        """
        Test that we cover an invalid format LEI
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INVALID_FORMAT_LEI_BOND, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_format_maturity_post(self):
        """
        Test that we cover an invalid maturity date
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INVALID_FORMAT_MATURITY_BOND, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_currency_post(self):
        """
        Test that we cover an invalid currency code
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INVALID_CURRENCY_BOND, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_size_post(self):
        """
        Test that we cover an size (negative)
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INVALID_SIZE_BOND, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_invalid_isin_post(self):
        """
        Test that we cover an invalid ISIN
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.INVALID_ISIN_BOND, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_double_posting(self):
        """
        Test that we cover double posting
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.VALID_BONDA, format="json")
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        resp = self.client.post(self.URL_POST, data=self.VALID_BONDA, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_double_posting_segregated(self):
        """
        Test that we cover double posting from different users
        """
        self._delete_all_bonds()
        self._login(self.USERA, self.PASSA)
        resp = self.client.post(self.URL_POST, data=self.VALID_BONDA, format="json")
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        self._login(self.USERB, self.PASSB)
        resp = self.client.post(self.URL_POST, data=self.VALID_BONDA, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_get(self):
        """
        Test getting a bond
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)

    def test_delete(self):
        """
        Test deleting a bond
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.delete(self.URL_DELETE(args=(self.VALID_BONDA['isin'],)))
        self.assertEqual(resp.status_code, 204)
        self.assertEqual(len(Bond.objects.all()), 0)

    def test_segregated_get(self):
        """
        Test users cannot get a bond from another user
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        self._login(self.USERB, self.PASSB)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertEqual(resp.status_code, 404)

    def test_segregated_delete(self):
        """
        Test users cannot delete a bond from another user
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        self._login(self.USERB, self.PASSB)
        resp = self.client.delete(self.URL_DELETE(args=(self.VALID_BONDA['isin'],)))
        self.assertEqual(resp.status_code, 404)

    def test_inexistent_delete(self):
        """
        Test users cannot delete an inexistent bond
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        resp = self.client.delete(self.URL_DELETE(args=(self.VALID_BONDA['isin'],)))
        self.assertEqual(resp.status_code, 404)

    def test_inexistent_get(self):
        """
        Test users cannot get an inexistent bond
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertEqual(resp.status_code, 404)

    def test_put(self):
        """
        Test updating a bond
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        resp = self.client.put(self.URL_PUT(args=(self.VALID_BONDA['isin'],)), data=self.VALID_BONDB, format="json")
        self.assertDictContainsSubset(self.VALID_BONDB, resp.data)

    def test_segregated_put(self):
        """
        Test users cannot update a bond from another user
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        self._login(self.USERB, self.PASSB)
        resp = self.client.put(self.URL_PUT(args=(self.VALID_BONDA['isin'],)), data=self.VALID_BONDB, format="json")
        self.assertEqual(resp.status_code, 404)

    def test_legal_name_update(self):
        """
        Test that the legal_name gets updated when the lei does
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        resp = self.client.put(self.URL_PUT(args=(self.VALID_BONDA['isin'],)), data=self.VALID_BONDB, format="json")
        full_valid_bondb = {
            **{'legal_name': self.VALID_BONDB_LEGAL_NAME},
            **self.VALID_BONDB
        }
        self.assertDictEqual(full_valid_bondb, resp.data)

    def test_illegal_key_update(self):
        """
        Test illegal keys in put call
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        resp = self.client.put(self.URL_PUT(args=(self.VALID_BONDA['isin'],)), data=self.INVALID_KEY_BOND, format="json")
        self.assertEqual(resp.status_code, 400)

    def test_illegal_legal_name_update(self):
        """
        Test illegal update of legal_names in put call
        """
        self._login(self.USERA, self.PASSA)
        self._delete_all_bonds()
        self._add_bond_model(self.VALID_BONDA, self.USERA)
        resp = self.client.get(self.URL_GET(args=(self.VALID_BONDA['isin'],)))
        self.assertDictContainsSubset(self.VALID_BONDA, resp.data)
        resp = self.client.put(self.URL_PUT(args=(self.VALID_BONDA['isin'],)), data=self.INVALID_LEGAL_NAME_KEY_BOND, format="json")
        self.assertEqual(resp.status_code, 400)
