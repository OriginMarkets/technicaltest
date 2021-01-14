import requests
from django.contrib.auth.models import User
from rest_framework import serializers
from django.conf import settings
from bonds.models import Bond


class BondSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Bond
        fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']
    
    def create(self, validated_data):

        gleif_url = settings.GLEIF_API_URL + validated_data['lei']  
        try:
            gleif_data = requests.get(gleif_url)
            legal_name = gleif_data.json()[0]['Entity']['LegalName']['$'] 
            validated_data['legal_name'] = legal_name
        
        except:
            validated_data['legal_name'] = "GLEIF_UNAVAILABLE"

        
        
        
        return super().create(validated_data)

