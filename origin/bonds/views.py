import requests
import json

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import Bonds
from .serializers import BondListSerializer, BondCreateSerializer


@permission_classes((IsAuthenticated,))
@api_view(['GET', 'POST'])
def bonds_data(request):
    """
    List all bonds, or create a new bond.
    """
    if request.method == 'GET':
        bonds = Bonds.objects.all()

        legal_name = request.query_params.get('legal_name')
        if legal_name:
            print('inside')
            print(legal_name)
            bonds = Bonds.objects.filter(legal_name__icontains=legal_name)

        serializer = BondListSerializer(bonds, many=True)
        print(request.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        lei = request.data['lei']
        legal_name = get_legal_name(lei)
        request.data['legal_name'] = legal_name

        serializer = BondCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HelloWorld(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request):
        return Response("Hello World!")


def get_legal_name(lei):
    url = 'https://leilookup.gleif.org/api/v2/leirecords?lei=%s' % lei

    response = requests.get(url)
    result = json.loads(response.content.decode('utf-8'))[0]

    legal_name = result['Entity']['LegalName']['$']

    if response.status_code == 200:
        return legal_name
    else:
        return None