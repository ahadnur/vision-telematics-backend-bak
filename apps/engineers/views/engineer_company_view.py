import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView

from apps.accounts.models import Company
from apps.engineers.serializers import EngineerCompanyListSerializer

logger = logging.getLogger(__name__)

class EngineerCompanyListAPIView(ListAPIView):
    queryset = Company.active_objects.filter(is_engineer_company=True)
    serializer_class = EngineerCompanyListSerializer
    pagination_class = None

    @swagger_auto_schema(
        tags=['Engineer Company'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of engineer companies with id and name',
                schema=EngineerCompanyListSerializer
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        logger.info('Fetching list of Engineer Companies')
        return self.list(request, *args, **kwargs)



class EngineerCompanyCreate(CreateAPIView):
    @swagger_auto_schema(
        tags=['Engineer Company'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Create engineer company',
                schema=EngineerCompanyListSerializer
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
