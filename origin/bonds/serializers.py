from django.conf import settings
import requests
from rest_framework import serializers

from bonds.models import Bond


class BondSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bond
        fields = ['isin', 'size', 'currency', 'maturity', 'lei', 'legal_name']

    def create(self, validated_data):
        gleif_url = settings.GLEIF_URL + '?lei=' + validated_data['lei']
        # NOTE: The line below may cause connection errors if gleif_url
        # is incorrect or unavailable. We're not catching this so that
        # it bubbles up and causes a 500 in the REST endpoint. However,
        # we may wish to handle this differently.
        gleif_data = requests.get(gleif_url)
        # NOTE: The line below may cause KeyError or IndexError if the
        # json from the GLEIF API comes back different than expected.
        # Atm assuming we want this to bubble up and cause a 500 in the
        # REST endpoint, however a different way of handling this might
        # be preferable.
        legal_name = gleif_data.json()[0]['Entity']['LegalName']['$']
        # NOTE: We're adding legal name to the validated data, which
        # isn't great as legal name hasn't actually been validated.
        # However, as this is not data supplied by the user, we're
        # assuming it is valid and if not that any database integrity
        # errors (such as the length of the legal name exceeding the db
        # limit) should bubble up and cause a 500 error on the endpoint.
        # This might not be the way to handle it, however.
        validated_data['legal_name'] = legal_name
        return super().create(validated_data)
