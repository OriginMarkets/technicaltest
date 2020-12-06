from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import DateField, ModelSerializer

from bonds.models import Bond


class BondSerializer(ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=CurrentUserDefault()
    )
    maturity = DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d"])

    class Meta:
        model = Bond
        fields = ["user", "isin", "size", "currency", "maturity", "lei", "legal_name"]
        extra_kwargs = {
            "legal_name": {"read_only": True},
        }

    def validate_isin(self, value):
        """
        Check that ISIN is 12 digits.
        """
        size = len(value)
        if size != 12:
            raise serializers.ValidationError(
                f"Error: ISIN needs to be of length 12 not {size}"
            )
        return value

    def validate_size(self, value):
        """
        Check that Size is 0 or more.
        """
        if value <= 0:
            raise serializers.ValidationError("Error: Size cannot be of size 0 or less")
        return value

    def validate_lei(self, value):
        """
        Check that LEI is 20 digits.
        """
        size = len(value)
        if size != 20:
            raise serializers.ValidationError(
                f"Error: LEI needs to be of length 20 not {size}"
            )
        return value

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
        bond_instance = Bond(**validated_data)
        bond_instance.user = user
        bond_instance.save()
        return bond_instance
