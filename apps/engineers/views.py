import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.engineers.models import Engineer, EngineerCompany
from apps.engineers.serializers import (EngieerCompanyListSerializer, EngineerWriteSerializer, EngineerReadSerializer,
                                        GetEngineerListSerializer)

logger = logging.getLogger(__name__)


class EngineerCompanyListAPIView(ListAPIView):
    queryset = EngineerCompany.active_objects.all()
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
    queryset = Engineer.active_objects.all().order_by('contact_name')
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
    queryset = Engineer.active_objects.all()
    serializer_class = EngineerWriteSerializer

    @swagger_auto_schema(
        tags=['Engineer'],
        operation_description="Create an Engineer with associated services and pricing",
        request_body=EngineerWriteSerializer,
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
    queryset = Engineer.active_objects.all()
    serializer_class = EngineerReadSerializer

    @swagger_auto_schema(
        tags=['Engineer'],
        operation_description="Retrieve an Engineer with associated services and pricing",
        responses={
            status.HTTP_200_OK: EngineerReadSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        }
    )
    def get(self, request, pk):
        try:
            engineer = Engineer.objects.get(id=pk)
            serializer = self.serializer_class(engineer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Engineer.DoesNotExist:
            logger.error(f'Engineer with id {pk} not found')
            return Response({'error': 'Engineer not found'}, status=status.HTTP_404_NOT_FOUND)


class EngineerUpdateAPIView(APIView):
    serializer_class = EngineerWriteSerializer

    @swagger_auto_schema(
        tags=['Engineer'],
        operation_description="Update an Engineer with associated services and pricing",
        request_body=EngineerWriteSerializer(),
        responses={
            status.HTTP_200_OK: EngineerWriteSerializer(),
            status.HTTP_400_BAD_REQUEST: "Bad Request"
        }
    )
    def put(self, request, pk):
        try:
            engineer = Engineer.active_objects.filter(id=pk).first()
            serializer = self.serializer_class(engineer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f'Engineer {pk} updated successfully')
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.warning(f'Engineer update failed due to validation error: {serializer.errors}')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Engineer.DoesNotExist:
            logger.error(f'Engineer with id {pk} not found for update')
            return Response({'error': 'Engineer not found'}, status=status.HTTP_404_NOT_FOUND)


class EngineerDestroyAPIView(DestroyAPIView):
    queryset = Engineer.active_objects.all()

    @swagger_auto_schema(
        tags=['Engineer'],
        responses={
            status.HTTP_204_NO_CONTENT: "Successfully deleted!",
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.is_active = False
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
