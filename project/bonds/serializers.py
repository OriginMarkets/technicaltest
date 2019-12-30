from typing import Dict

from rest_framework import fields, serializers
from rest_framework.exceptions import ValidationError

from project.bonds.models import Bond, LegalEntity
from project.bonds.client import GliefClient


class BondSerializer(serializers.ModelSerializer):
    lei = fields.CharField(required=True, min_length=20, max_length=20)

    class Meta:
        model = Bond
        fields = ["isin", "size", "currency", "maturity", "lei"]

    def create(self, validated_data: Dict) -> Bond:
        user_id = self.context["user_id"]
        lei = validated_data.pop("lei")
        client = GliefClient()
        legal_entity_data = client.lei_lookup(lei)
        try:
            legal_entity_instance = LegalEntity.objects.get(
                legal_name=legal_entity_data["legal_name"],
            )
        except LegalEntity.DoesNotExist:
            legal_entity_instance = LegalEntity.objects.create(**legal_entity_data)

        bond_instance = Bond.objects.create(
            **validated_data, user_id=user_id, legal_entity=legal_entity_instance
        )

        return bond_instance

    def validate(self, data: Dict) -> Dict:
        """
        Check the unique constaint on user and isin.
        """
        validated_data = super().validate(data)
        isin = validated_data["isin"]
        user_id = self.context["user_id"]
        try:
            Bond.objects.get(isin=isin, user_id=user_id)
        except Bond.DoesNotExist:
            return validated_data

        raise ValidationError(detail="isin already exists.", code="isin")

    def to_representation(self, bond: Bond) -> Dict:
        return {
            "isin": bond.isin,
            "size": bond.size,
            "currency": bond.currency,
            "maturity": bond.maturity.isoformat(),
            "lei": bond.legal_entity.lei,
            "legal_name": bond.legal_entity.legal_name,
        }
