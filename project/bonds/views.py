import logging
from typing import Dict

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from project.bonds.models import Bond, LegalEntity
from project.bonds.serializers import BondSerializer

logger = logging.getLogger(__name__)


class BondListView(APIView):
    permission_classes = [IsAuthenticated]

    def filter_queryset(self, query_params: Dict, queryset: Bond) -> Bond:
        lei_filter = query_params.get("lei")
        legal_name_filter = query_params.get("legal_name")

        if lei_filter:
            logger.debug("Filtering by LEI")

            try:
                legal_entity = LegalEntity.objects.get(lei=lei_filter)
            except LegalEntity.DoesNotExist:
                legal_entity = None

            bonds_matching_lei = queryset.filter(legal_entity=legal_entity)
            return bonds_matching_lei

        if legal_name_filter:
            try:
                legal_entity = LegalEntity.objects.get(legal_name=legal_name_filter)
            except LegalEntity.DoesNotExist:
                legal_entity = None

            bonds_matching_lei = queryset.filter(legal_entity=legal_entity)
            return bonds_matching_lei

        logger.debug("No matching filters")
        return queryset

    def get_queryset(self, request: Request) -> Bond:
        return Bond.objects.filter(user=request.user).order_by("created")

    def get(self, request: Request) -> Response:
        queryset = self.get_queryset(request)
        queryset = self.filter_queryset(request.query_params, queryset)

        serializer = BondSerializer(
            many=True, instance=queryset, context={"user_id": request.user.id}
        )
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = BondSerializer(data=request.data, context={"user_id": request.user.id})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({"id": str(instance.id)}, status=status.HTTP_201_CREATED)
