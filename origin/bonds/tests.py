from rest_framework.test import APISimpleTestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.test import TestCase


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200

class BondsTest(APISimpleTestCase, TestCase):
    def setUp(self):
        User.objects.create(username='svet', email='svet@tsvet.com', password='svet234')
        user = User.objects.get(username='svet')
        Token.objects.create(user=user)

    def test_unathorised_access(self):
        response = self.client.get("/bonds/")
        assert response.status_code == 401

    def test_bonds_index_view(self):
        token = Token.objects.get(user__username='svet')
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get("/bonds/")
        assert response.status_code == 200
