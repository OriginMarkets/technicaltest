from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models
from . import serializers


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class ListCreateBonds(APIView):
    def get(self, request, format=None):
        bonds = models.Bond.objects.filter(user=request.user)
        legal_name = self.request.query_params.get('legal_name', None)
        if legal_name is not None:
            bonds = bonds.filter(legal_name=legal_name)
        serializer = serializers.BondSerializer(bonds, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = serializers.BondSerializer(data=request.data)
        request.data['user'] = request.user.id
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
