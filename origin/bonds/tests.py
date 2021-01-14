
from django.contrib.auth.models import User

from django.test.testcases import SerializeMixin
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate, APIClient
from django.urls import reverse
from bonds.models import Bond
from bonds.serializers import BondSerializer

   

class BondViewTestCase(APITestCase):
    url = '/bonds/'

    def setUp(self):
        
        self.user = User.objects.create_user(username="charles", password="some-very-strong-psw")
        #self.user1 =  User.objects.create_user(username="charles2", password="some-very-strong-psw")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)



    def create_bond(self):
        #bond 1 lei is R0MUWSFPU8MPRO8K5P83 legal name is BNP PARIBAS
        bond1 = {"isin": "FR0000131104","size": 100000000,"currency": "EUR","maturity": "2025-02-28","lei": "R0MUWSFPU8MPRO8K5P83"}
        response = self.client.post(self.url, bond1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['isin'],"FR0000131104")
        self.assertEqual(response.data['size'],100000000)
        self.assertEqual(response.data['currency'],"EUR")
        self.assertEqual(response.data['maturity'],"2025-02-28")
        self.assertEqual(response.data['lei'],"R0MUWSFPU8MPRO8K5P83")
        
        #bond 2 lei is 261700K5E45DJCF5Z735 legal name is APIR SYSTEMS LIMITED
        bond2 = {"isin": "FR0000131104","size": 100000000,"currency": "GBP","maturity": "2025-02-28","lei": "261700K5E45DJCF5Z735"}
        response = self.client.post(self.url, bond2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #bond 3 lei is R0MUWSFPU8MPRO8K5P83 legal name is BNP PARIBAS
        bond3 = {"isin": "FR0000131104","size": 100000000,"currency": "GBP","maturity": "2025-02-28","lei": "R0MUWSFPU8MPRO8K5P83"}
        response = self.client.post(self.url, bond3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bond.objects.count(),3)

   
    def list_bond(self):
        
        response = self.client.get(self.url)
        print("list")
        print(response.data)
        self.assertEqual(len(response.data),2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['isin'],"FR0000131104")
        self.assertEqual(response.data[0]['size'],100000000)
        self.assertEqual(response.data[0]['currency'],"EUR")
        self.assertEqual(response.data[0]['maturity'],"2025-02-28")
        self.assertEqual(response.data[0]['lei'],"R0MUWSFPU8MPRO8K5P83")
        self.assertEqual(response.data[0]['legal_name'],'BNP PARIBAS')
        
        
    def list_unauthorized(self):
        new_client = APIClient()
        response_NewClient = new_client.get(path="/bonds/")
        self.assertEqual(response_NewClient.status_code, status.HTTP_403_FORBIDDEN)

    def list_for_different_owner(self):
        ##bond 4 lei is NKY7JRBKJHQQ68KJ6252 legal name is GLOBAL MACRO ABSOLUTE RETURN ADVANTAGE PORTFOLIO
        bond4 = {"isin": "GB0000131104","size": 100000000,"currency": "GBP","maturity": "2025-02-28","lei": "NKY7JRBKJHQQ68KJ6252"}    
        user2 = User.objects.create_user(username="charles2", password="some-very-strong-psw")
        new_client = APIClient()
        new_client.force_authenticate(user=user2)
        
        response_NewClient = new_client.post(path="/bonds/",data=bond4)
        self.assertEqual(Bond.objects.count(),4)
        response_NewClient = new_client.get(path="/bonds/")
        self.assertEqual(response_NewClient.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_NewClient.data),1)
        print("new client")
        print(response_NewClient.data)
        


    def filter_legal_name(self):
        legal_name = "BNP PARIBAS"
        filtering_url = self.url + "?" + legal_name

        response = self.client.get(filtering_url)
  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for i in range(len(response.data)):
            self.assertEqual(response.data[i]["legal_name"],legal_name)    

    def test_bond_list_and_create(self):
        self.create_bond()
        self.list_bond()
        self.list_unauthorized()
        self.list_for_different_owner()
        self.filter_legal_name()



        




    