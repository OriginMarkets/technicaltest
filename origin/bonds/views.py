from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from bonds.serializers import BondSerializer
from bonds.models import Bond


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class BondViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    # BasicAuthentication is probably the worst possible auth but with it I can avoid doing more setup for tokens
    # or building log in interface for session auth to use in browser
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Bond.objects.all()
    serializer_class = BondSerializer

    def get_queryset(self):
        queryset = Bond.objects.filter(user=self.request.user).select_related('legal_entity')
        legal_name = self.request.query_params.get('legal_name', None)
        if legal_name is not None:
            # for now just simplest exact match filter
            queryset = queryset.filter(legal_entity__legal_name=legal_name)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
