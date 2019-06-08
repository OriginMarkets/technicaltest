from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.reverse import reverse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from bonds.models import Bond
from django.conf import settings


def error(message, status):
    return Response({'error': message}, status=status)


class BondSerializer(ModelSerializer):
    class Meta:
        model = Bond
        exclude = ('user',)
        depth = 0


class BondViewSet(object):

    class BondViewList(APIView):
        authentication_classes = (SessionAuthentication, TokenAuthentication)
        permission_classes = (IsAuthenticated,)

        def get(self, request):
            legal_name_filter = request.GET.get("legal_name", None)
            if legal_name_filter:
                bonds = Bond.objects.filter(
                    legal_name__icontains=legal_name_filter,
                    user=request.user
                )
            else:
                bonds = Bond.objects.filter(
                    user=request.user
                )
            serializer_list = [BondSerializer(bond).data for bond in bonds]
            return Response(serializer_list, status=status.HTTP_200_OK)

        def post(self, request):
            try:
                request_values = request.data.items()
                for request_key, request_value_update in request_values:
                    if not (
                        hasattr(Bond, request_key) and
                        request_key not in Bond.readonly_fields
                    ):
                        return error(
                            'Key {} is invalid or readonly'.format(request_key),
                            status=status.HTTP_400_BAD_REQUEST
                        )
                bond = Bond(user=request.user,**request.data)
                bond.save()
                serializer = BondSerializer(bond)
                headers = {'Location': reverse('bonds-id', (bond.isin,))}
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )

            except (ValidationError, TypeError) as e:
                return error(str(e), status=status.HTTP_400_BAD_REQUEST)

    class BondViewDetail(APIView):
        authentication_classes = (SessionAuthentication, BasicAuthentication)
        permission_classes = (IsAuthenticated,)

        def get(self, request, isin):
            try:
                bond = Bond.objects.get(isin=isin, user=request.user)
                serializer = BondSerializer(bond)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return error('ISIN not found', status=status.HTTP_404_NOT_FOUND)

        def delete(self, request, isin):
            try:
                bond = Bond.objects.get(isin=isin, user=request.user)
                bond.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ObjectDoesNotExist:
                return error('ISIN not found', status=status.HTTP_404_NOT_FOUND)

        def put(self, request, isin):
            try:
                request_values = request.data.items()
                bond = Bond.objects.get(isin=isin, user=request.user)
                for request_key, request_value_update in request_values:
                    if (
                        hasattr(bond, request_key) and
                        request_key not in Bond.readonly_fields
                    ):
                        setattr(bond, request_key, request_value_update)
                    else:
                        return error(
                            'Key {} is invalid or readonly'.format(request_key),
                            status=status.HTTP_400_BAD_REQUEST
                        )

                bond.save()
                serializer = BondSerializer(bond)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return error('ISIN not found', status=status.HTTP_404_NOT_FOUND)
