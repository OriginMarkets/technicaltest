from rest_framework import serializers

from bonds.models import Bond

from bonds.models import LegalEntity

from bonds.logic import fetch_legal_entity_name


class BondSerializer(serializers.ModelSerializer):
    lei = serializers.CharField(max_length=50, source='legal_entity.lei')
    legal_name = serializers.CharField(max_length=200, read_only=True, source='legal_entity.legal_name')

    class Meta:
        model = Bond
        fields = ('id', 'isin', 'size', 'currency', 'maturity', 'lei', 'legal_name')
        
    def create(self, validated_data):
        lei = validated_data['legal_entity']['lei']
        legal_entity = LegalEntity.objects.filter(lei=lei).first()
        if not legal_entity:
            # do not linger on external API call so we can return swiftly to client,
            # if failed to get name then this job should be now put on some async processing queue
            # to fetch the name and update the record at later point
            legal_name = fetch_legal_entity_name(lei, timeout=1)
            legal_entity = LegalEntity.objects.create(lei=lei, legal_name=legal_name)
        
        validated_data['legal_entity'] = legal_entity
        return super(BondSerializer, self).create(validated_data)
