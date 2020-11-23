from rest_framework.serializers import ModelSerializer
from bonds.models import Bonds


class BondListSerializer(ModelSerializer):
    class Meta:
        model = Bonds
        fields = [
            'isin',
            'size',
            'currency',
            'maturity',
            'lei',
            'legal_name'
        ]

class BondCreateSerializer(ModelSerializer):
    class Meta:
        model = Bonds
        fields = [
            'isin',
            'size',
            'currency',
            'maturity',
            'lei',
            'legal_name'
        ] 