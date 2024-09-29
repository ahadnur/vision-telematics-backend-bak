from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.customers.models import CustomerCompany, Customer
from apps.customers.serializers import (CompanyListSerializer, CustomerWriteSerializer, CustomerVehicleSerializer)
from apps.customers.schemas import vehicle_info_response_schema
from apps.utilities.models import VehicleMake, VehicleModel, VehicleType
import logging
logger = logging.getLogger(__name__)


class CompanyListAPIView(ListAPIView):
    queryset = CustomerCompany.objects.filter(is_active=True)
    serializer_class = CompanyListSerializer

    @swagger_auto_schema(
        tags=['Company List'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='List of companies with id and name',
                schema=CompanyListSerializer(many=True)
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CustomerCreateAPIView(views.APIView):
    @swagger_auto_schema(
        tags=['Customer'],
        request_body=CustomerWriteSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Created customer',
                schema=CustomerWriteSerializer
            )
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = CustomerWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Customer created successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"create customer error on {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CustomerUpdateAPIView(views.APIView):
    @swagger_auto_schema(
        tags=['Customer'],
        request_body=CustomerWriteSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Created customer',
                schema=CustomerWriteSerializer
            )
        }
    )
    def post(self, request, pk):
        try:
            customer = Customer.objects.get(id=pk)
            serializer = CustomerWriteSerializer(instance=customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Customer updated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"create customer error on {e}")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateCustomerVehicleAPIView(views.APIView):

    @swagger_auto_schema(
        tags=['Customer'],
        request_body=CustomerVehicleSerializer,
    )
    def post(self, request, *args, **kwargs):
        pass


class GetVehicleInfoAPIView(views.APIView):
    # permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        tags=['Customer'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Vehicle info',
                schema=vehicle_info_response_schema
            )
        }
    )
    def get(self, request):
        try:

            vehicle_make = VehicleMake.objects.values_list('id', 'vehicle_make')
            vehicle_model = VehicleModel.objects.values_list('id', 'vehicle_model')
            vehicle_type = VehicleType.objects.values_list('id', 'vehicle_type')
            data = {
                'vehicle_makes': vehicle_make,
                'vehicle_models': vehicle_model,
                'vehicle_types': vehicle_type
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(str(e),exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

