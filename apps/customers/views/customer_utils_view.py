import logging

from django.db.models import F
from drf_yasg import openapi
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.customers.schemas import customer_dropdown_response_schema, customer_vehicle_list_response_schema
from apps.customers.serializers import CustomerDropdownSerializer, CustomerVehicleSerializer, \
	CustomerVehicleListSerializer, CustomerSpecificVehicleSerializer
from apps.customers.models import Customer, CustomerVehicle


logger = logging.getLogger(__name__)

class CustomerDropdownListAPIView(ListAPIView):
	serializer_class = CustomerDropdownSerializer
	queryset = Customer.active_objects.all()
	pagination_class = None

	@swagger_auto_schema(
		tags=['Customer'],
		operation_summary="Retrieve Customer Dropdown List",
		operation_description="Returns a list of active customer IDs and names for dropdowns or selection components.",
		responses={
			status.HTTP_200_OK: customer_dropdown_response_schema
		}
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)


class CustomerVehicleListAPIView(ListAPIView):
	serializer_class = CustomerVehicleListSerializer
	queryset = CustomerVehicle.active_objects.order_by('-created_at')

	def get_queryset(self):
		return CustomerVehicle.active_objects.annotate(
			customer_name=F('customer__contact_name'),
			make=F('vehicle_make__make_name'),
			model=F('vehicle_model__name'),
			type=F('vehicle_type__type_name'),
		).values('id', 'registration_number', 'customer_name', 'make', 'model', 'type', )

	@swagger_auto_schema(
		tags=['Customer'],
		operation_summary="Retrieve Vehicle List",
		responses={
			status.HTTP_200_OK: customer_vehicle_list_response_schema
		}
	)
	def get(self, request, *args, **kwargs):
		paginated = request.query_params.get('paginated', 'true').lower() == 'true'
		if not paginated:
			self.pagination_class = None
		return self.list(request, *args, **kwargs)


class CustomerSpecificVehicleListAPIView(APIView):

	@swagger_auto_schema(
		tags=['Customer'],
		responses={
			status.HTTP_200_OK: openapi.Response(
				description='Get customer vehicle list',
				schema=CustomerSpecificVehicleSerializer
			)
		}
	)
	def get(self, request, customer_id, *args, **kwargs):
		try:
			queryset = CustomerVehicle.active_objects.filter(
				customer_id=customer_id,
			).select_related('vehicle_model', 'vehicle_make', 'vehicle_type')
			serializer = CustomerSpecificVehicleSerializer(queryset, many=True)
			return Response(serializer.data)
		except CustomerVehicle.DoesNotExist:
			logger.error(f'Customer {customer_id} does not exist')
			return Response(status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			logger.error(f'Customer {customer_id} has an error: {e}')
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

