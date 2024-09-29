import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.engineers.models import Engineer, EngineerCompany
from apps.engineers.serializers import (EngieerCompanyListSerializer, EngineerWriteSerializer, EngineerReadSerializer,
                                        GetEngineerListSerializer)

logger = logging.getLogger(__name__)


class EngineerCompanyListAPIView(ListAPIView):
    queryset = EngineerCompany.objects.filter(is_active=True)
    serializer_class = EngieerCompanyListSerializer
    pagination_class = None

    @swagger_auto_schema(
        tags=['Engineer'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of engineer companies with id and name',
                schema=EngieerCompanyListSerializer
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        logger.info('Fetching list of Engineer Companies')
        return self.list(request, *args, **kwargs)


class EngineerListAPIView(ListAPIView):
    queryset = Engineer.objects.filter(is_active=True).order_by('contact_name')
    serializer_class = GetEngineerListSerializer

    @swagger_auto_schema(
        tags=['Engineer'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of engineer companies with id and name',
                schema=GetEngineerListSerializer(many=True)
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EngineerCreateAPIView(CreateAPIView):
    queryset = Engineer.objects.filter(is_active=True)
    serializer_class = EngineerWriteSerializer

    @swagger_auto_schema(
        tags=['Engineer'],
        operation_description="Create an Engineer with associated services and pricing",
        request_body=EngineerReadSerializer,
        responses={
            status.HTTP_201_CREATED: "Successfully engineer created!",
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        logger.info('Creating a new Engineer')
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            logger.info('Engineer created successfully')
        else:
            logger.warning(f'Engineer creation failed with status {response.status_code}')
        return response


class EngineerRetrieveAPIView(APIView):
    queryset = Engineer.objects.all()
    serializer_class = EngineerWriteSerializer

    @swagger_auto_schema(
        tags=['Engineer'],
        operation_description="Retrieve an Engineer with associated services and pricing",
        responses={
            status.HTTP_200_OK: EngineerReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        }
    )
    def get(self, request, *args, **kwargs):
        logger.info(f'Retrieving Engineer details for id: {kwargs.get("pk")}')
        try:
            engineer = Engineer.objects.get(pk=kwargs.get('pk'))
            serializer = self.serializer_class(engineer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Engineer.DoesNotExist:
            logger.error(f'Engineer with id {kwargs.get("pk")} not found')
            return Response({'error': 'Engineer not found'}, status=status.HTTP_404_NOT_FOUND)


class EngineerUpdateAPIView(APIView):
    serializer_class = EngineerWriteSerializer

    @swagger_auto_schema(
        operation_description="Update an Engineer with associated services and pricing",
        responses={
            status.HTTP_200_OK: EngineerReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        }
    )
    def put(self, request, *args, **kwargs):
        logger.info(f'Updating Engineer with id: {kwargs.get("pk")}')
        try:
            engineer = Engineer.objects.get(pk=kwargs.get('pk'))
            serializer = self.serializer_class(engineer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f'Engineer {kwargs.get("pk")} updated successfully')
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.warning(f'Engineer update failed due to validation error: {serializer.errors}')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Engineer.DoesNotExist:
            logger.error(f'Engineer with id {kwargs.get("pk")} not found for update')
            return Response({'error': 'Engineer not found'}, status=status.HTTP_404_NOT_FOUND)

