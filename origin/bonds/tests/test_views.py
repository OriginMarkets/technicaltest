import datetime
import json
from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APISimpleTestCase, APITestCase

from bonds.models import Bond, LegalEntity, CURRENCIES
from bonds.serializers import BondSerializer

User = get_user_model()


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200


class BondViewSetTestCase(APITestCase):
    def setUp(self):
        # normally I would use factory boy and create a factory for each new model
        # but for this simple exercise I think that can be skipped
        self.legal_entity = LegalEntity.objects.create(lei='fake', legal_name='Huge funds')
        self.user1 = User.objects.create(username='customer1')
        self.user1.set_password('foobar123')
        self.user1.save()
        self.user2 = User.objects.create(username='customer2')

        self.bond1 = Bond.objects.create(
            user=self.user1,
            legal_entity=self.legal_entity,
            isin='HH123',
            size=8000000,
            currency=CURRENCIES.EUR.value,
            maturity=datetime.date(2019, 5, 10)
        )

        self.bond2 = Bond.objects.create(
            user=self.user1,
            legal_entity=LegalEntity.objects.create(lei='fake2', legal_name='Big funds'),
            isin='HH123123',
            size=3000000,
            currency=CURRENCIES.EUR.value,
            maturity=datetime.date(2019, 5, 10)
        )

        self.bond3 = Bond.objects.create(
            user=self.user2,
            legal_entity=self.legal_entity,
            isin='UJH123',
            size=9000000,
            currency=CURRENCIES.GBP.value,
            maturity=datetime.date(2019, 5, 11)
        )

    def test_bond_list_when_not_authenticated(self):
        resp = self.client.get(reverse('bond-list'))
        self.assertEqual(resp.status_code, 403)

    def test_bond_list_only_own_records(self):
        self.client.login(username='customer1', password='foobar123')
        resp = self.client.get('{}?legal_name={}'.format(reverse('bond-list'), self.legal_entity.legal_name))
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(
            resp.content,
            [{'id': 1,
              'isin': 'HH123',
              'size': '8000000.00',
              'currency': CURRENCIES.EUR.value,
              'maturity': '2019-05-10',
              'lei': 'fake',
              'legal_name': 'Huge funds'}]
        )

    def test_bond_create_legal_entity_already_exists(self):
        self.client.login(username='customer1', password='foobar123')
        bond_count_before = Bond.objects.filter(user=self.user1).count()
        resp = self.client.post(
            reverse('bond-list'),
            data=json.dumps({
                'isin': 'HJK213123',
                'size': 10000000,
                'currency': CURRENCIES.EUR.value,
                'maturity': '2019-05-10',
                'lei': self.legal_entity.lei
            }),
            content_type='application/json'
        )

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Bond.objects.filter(user=self.user1).count(), bond_count_before + 1)


class BondSerializerTestCase(TestCase):
    def setUp(self):
        self.legal_entity = LegalEntity.objects.create(lei='fake', legal_name='Huge funds')
        self.user1 = User.objects.create(username='customer1')

    @patch('bonds.serializers.fetch_legal_entity_name')
    def test_create_when_legal_entity_already_exists(self, mock_fetch_legal_entity_name):
        serializer = BondSerializer()
        created_bond = serializer.create(
            {
                'isin': 'HH787687',
                'size': 12000000,
                'currency': CURRENCIES.EUR,
                'maturity': datetime.date(2019, 5, 12),
                # this is the format data will be constructed by the serializer
                'legal_entity': {'lei': self.legal_entity.lei},
                # this is set when called serializer's save method with it as kwarg
                'user': self.user1
            }
        )

        self.assertEqual(created_bond.legal_entity, self.legal_entity)
        self.assertEqual(mock_fetch_legal_entity_name.call_count, 0)

    @patch('bonds.serializers.fetch_legal_entity_name', Mock(return_value='Small funds'))
    def test_create_when_legal_entity_does_not_exist(self):
        serializer = BondSerializer()
        legal_entity_count = LegalEntity.objects.count()
        created_bond = serializer.create(
            {
                'isin': 'HH787687',
                'size': 12000000,
                'currency': CURRENCIES.EUR,
                'maturity': datetime.date(2019, 5, 12),
                # this is the format data will be constructed by the serializer
                'legal_entity': {'lei': 'new_lei'},
                # this is set when called serializer's save method with it as kwarg
                'user': self.user1
            }
        )

        self.assertEqual(LegalEntity.objects.count(), legal_entity_count + 1)
        legal_entity = LegalEntity.objects.get(lei='new_lei')
        self.assertEqual(legal_entity.legal_name, 'Small funds')
        self.assertEqual(created_bond.legal_entity, legal_entity)
