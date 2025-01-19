from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView

from apps.customers.models import Customer, CustomerVehicle
from apps.customers.serializers import CustomerVehicleDropdownForOrderSerializer


class CustomerVehicleForOrderDropdown(RetrieveAPIView):
	queryset = CustomerVehicle.active_objects.all()
	serializer_class = CustomerVehicleDropdownForOrderSerializer
	lookup_field = 'customer_id'

	def get_queryset(self, *args, **kwargs):
		return CustomerVehicle.active_objects.select_related('vehicle_make').filter(
			id=self.kwargs.get(self.lookup_field)
		).distinct().values('id', 'vehicle_make')
	@swagger_auto_schema(
		tags=['Orders'],
		responses={
			status.HTTP_200_OK: openapi.Schema(
				type=openapi.TYPE_OBJECT,
				properties={
					'id': openapi.Schema(type=openapi.TYPE_INTEGER),
					'vehicle_make': openapi.Schema(type=openapi.TYPE_STRING),
				}
			)
		}
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class CustomerVehicleModelForOrderDropdown(RetrieveAPIView):
	queryset = CustomerVehicle.active_objects.all()
	lookup_field = 'vehicle_make_id'

	def get_queryset(self, *args, **kwargs):
		return CustomerVehicle.active_objects.select_related('vehicle_make').filter(
			vehicle_make_id=self.kwargs.get(self.lookup_field)
		).values('id', 'vehicle_model', 'vehicle_type', 'registration_number')

	@swagger_auto_schema(
		tags=['Orders'],
		responses={
			status.HTTP_200_OK: openapi.Schema(
				type=openapi.TYPE_OBJECT,
				properties={
					'id': openapi.Schema(type=openapi.TYPE_INTEGER),
					'vehicle_model': openapi.Schema(type=openapi.TYPE_STRING),
					'vehicle_type': openapi.Schema(type=openapi.TYPE_STRING),
					'registration_number': openapi.Schema(type=openapi.TYPE_STRING),
				}
			)
		}
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)