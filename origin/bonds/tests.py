from django.urls import reverse
from rest_framework.test import APISimpleTestCase
from rest_framework import status
from rest_framework.test import APITestCase

from . import models


class HelloWorld(APISimpleTestCase):
    def test_root(self):
        resp = self.client.get("/")
        assert resp.status_code == 200


class BondsTests(APITestCase):
    def test_bond_list(self):
        url = reverse('bonds')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_bonds(self):
        url = reverse('bonds')
        data = {
            "isin": "FR0000131104",
            "size": 100000000,
            "currency": "EUR",
            "maturity": "2025-02-28",
            "lei": "R0MUWSFPU8MPRO8K5P83"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Bond.objects.count(), 1)
        self.assertEqual(models.Bond.objects.get().isin, 'FR0000131104')
