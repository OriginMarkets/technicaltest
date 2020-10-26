import requests
import json
from bonds.models import PostBond
from rest_framework import serializers
from leipy import GLEIF

class BondSerializer(serializers.ModelSerializer):
    legal_name = serializers.SerializerMethodField()
    class Meta:
        model = PostBond
        fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']

    def get_legal_name(self, obj):
        queryset = PostBond.objects.all()

        for query in queryset:
            query_lei = query.lei
            gleif = GLEIF(api_version='v2')
            raw_output, results, results_df = gleif.request(
                [query_lei],
                return_dataframe=True
            )
        legal_name = results.legal_name
        return legal_name
