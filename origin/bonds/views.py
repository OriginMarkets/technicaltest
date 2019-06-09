from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ModelSerializer
from rest_framework.reverse import reverse
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from bonds.models import Bond


def error(message: str, status: int) -> Response:
    """
    Helper function to return JSON error responsesa

    :param message: The message you want to pass
    :param status: The status code you want to respond with
    """
    return Response({'detail': message}, status=status)


class BondSerializer(ModelSerializer):
    """
    Serializer definition, we want to serialize everything except for the user
    """
    class Meta:
        model = Bond
        exclude = ('user',)
        depth = 0


class BondViewSet(object):
    """
    Just a class to wrap all the BondViews
    """

    class BondViewList(APIView):
        """
        This the view for list and post operation where we allow only Session and
        Token authentication methods, allowing to do everything if logged in
        """
        authentication_classes = (SessionAuthentication, TokenAuthentication)
        permission_classes = (IsAuthenticated,)

        def get(self, request):
            """
            Get handler for listing the bonds of a user

            # TODO: Pagination
            """
            # We check wheter we have a filter and retrieve with that filter
            # otherwise return all bonds of that user
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
            # Serialize the bonds one by one
            serializer_list = [BondSerializer(bond).data for bond in bonds]
            # Return the serialzer list
            return Response(serializer_list, status=status.HTTP_200_OK)

        def post(self, request):
            """
            Post handler for posting bonds
            """
            try:
                # Retrieve the items of the request, check they exist on the
                # model and that they are not readonly, otherwise Bad Request
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
                # Create the bond attached to the user, serialize and return
                # the location of the newly created object
                bond = Bond(user=request.user,**request.data)
                bond.save()
                serializer = BondSerializer(bond)
                headers = {'Location': reverse('bonds-gud', (bond.isin,))}
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                    headers=headers
                )

            except (ValidationError, TypeError) as e:
                return error(str(e), status=status.HTTP_400_BAD_REQUEST)

    class BondViewDetail(APIView):
        """
        This the view for identifiable bonds, so we can update, delete, and get them
        we allow only Session and Token authentication methods,
        allowing to do everything if logged in
        """
        authentication_classes = (SessionAuthentication, TokenAuthentication)
        permission_classes = (IsAuthenticated,)

        def get(self, request, isin):
            """
            Simple get handler, taking care of not exising ISINs
            """
            try:
                bond = Bond.objects.get(isin=isin, user=request.user)
                serializer = BondSerializer(bond)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return error('ISIN not found', status=status.HTTP_404_NOT_FOUND)

        def delete(self, request, isin):
            """
            Simple delete handler, taking care of not exising ISINs
            """
            try:
                bond = Bond.objects.get(isin=isin, user=request.user)
                bond.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ObjectDoesNotExist:
                return error('ISIN not found', status=status.HTTP_404_NOT_FOUND)

        def put(self, request, isin):
            """
            Put handler for bonds, we must check that we have the keys we are going
            to update and they aren't readonly
            """
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
