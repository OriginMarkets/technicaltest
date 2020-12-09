
from rest_framework.viewsets import ModelViewSet
from .models import Bond
from .serializers import BondSerializer


class BondViewSet(ModelViewSet):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer
