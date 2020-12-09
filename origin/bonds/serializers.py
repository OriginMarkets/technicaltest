from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    CharField,
)

from .models import Bond
from users.models import InternalUser

# For consistency with standard json naming conventions
# - Opt to use id over pk
# - Rename legal_name to legalName 
class BondSerializer(ModelSerializer):

    user = PrimaryKeyRelatedField(
        queryset=InternalUser.objects.all()
    )

    legalName = CharField(source="legal_name", read_only=True)


    class Meta:
        model = Bond

        fields = [
            "id",
            "user",
            "created",
            "isin",
            "size",
            "currency",
            "maturity",
            "lei",
            "legalName",
        ]
