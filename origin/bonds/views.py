from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from bonds.models import Bond
from bonds.serializers import BondSerializer


class HelloWorld(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        return Response("Hello World!")


class BondAPIView(ListCreateAPIView):
    """List bonds or create a new bond"""

    serializer_class = BondSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Filter by legal_name if it's passed in
        """
        legal_name = self.request.query_params.get("legal_name", None)
        if legal_name is not None:
            queryset = Bond.objects.all().filter(
                user=self.request.user, legal_name=legal_name
            )
        else:
            queryset = Bond.objects.all().filter(user=self.request.user)

        return queryset
