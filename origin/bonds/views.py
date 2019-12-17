from rest_framework.generics import ListCreateAPIView

from bonds.models import Bond
from bonds.serializers import BondSerializer


class BondListCreateView(ListCreateAPIView):
    queryset = Bond.objects.all()
    serializer_class = BondSerializer

    def filter_queryset(self, queryset):
        """Filter bonds by current user and legal name (if provided as a GET param)"""
        queryset = super().filter_queryset(queryset).filter(user=self.request.user)
        if 'legal_name' in self.request.GET:
            return queryset.filter(legal_name=self.request.GET['legal_name'])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
