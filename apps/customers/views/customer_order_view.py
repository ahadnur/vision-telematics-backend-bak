from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView

from apps.customers.models import CustomerVehicle
from apps.customers.serializers import CustomerVehicleMakerSerializer, CustomerVehicleModelSerializer


class CustomerVehicleForOrderDropdown(ListAPIView):
	queryset = CustomerVehicle.active_objects.all()
	serializer_class = CustomerVehicleMakerSerializer
	lookup_field = 'customer_id'

	def get_queryset(self, *args, **kwargs):
		return CustomerVehicle.active_objects.select_related('vehicle_make').filter(
			id=self.kwargs.get(self.lookup_field)
		).distinct()

	@swagger_auto_schema(
		tags=['Orders'],
		manual_parameters=[
			openapi.Parameter(
				'paginated',
				openapi.IN_QUERY,
				description="Enable or disable pagination (true or false)",
				type=openapi.TYPE_BOOLEAN,
				required=False,
				default=True
			),
		],
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
		paginated = request.query_params.get('paginated', 'true').lower() == 'true'
		if not paginated:
			self.pagination_class = None
		return self.list(request, *args, **kwargs)


class CustomerVehicleModelForOrderDropdown(ListAPIView):
	queryset = CustomerVehicle.active_objects.all()
	serializer_class = CustomerVehicleModelSerializer
	lookup_field = 'vehicle_make_name'

	def get_queryset(self, *args, **kwargs):
		queryset = (CustomerVehicle.active_objects.select_related('vehicle_make', 'vehicle_model', 'vehicle_type')
		.filter(
			vehicle_make__make_name=self.kwargs.get(self.lookup_field)
		))
		return queryset

	@swagger_auto_schema(
		tags=['Orders'],
		manual_parameters=[
			openapi.Parameter(
				'paginated',
				openapi.IN_QUERY,
				description="Enable or disable pagination (true or false)",
				type=openapi.TYPE_BOOLEAN,
				required=False,
				default=True
			),
		],
	)
	def get(self, request, *args, **kwargs):
		paginated = request.query_params.get('paginated', 'true').lower() == 'true'
		if not paginated:
			self.pagination_class = None
		return self.list(request, *args, **kwargs)