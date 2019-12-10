from rest_framework import serializers

from . import models


class BondSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bond
        fields = (
            'isin',
            'size',
            'currency',
            'maturity',
            'lei',
            'legal_name',
            'user',
        )
