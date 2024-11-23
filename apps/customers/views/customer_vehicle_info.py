from rest_framework import status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.customers.serializers import CustomerVehicleSerializer
from apps.customers.schemas import vehicle_info_response_schema
from apps.utilities.models import VehicleMake, VehicleModel, VehicleType
import logging


logger = logging.getLogger(__name__)


class CreateCustomerVehicleAPIView(APIView):

	@swagger_auto_schema(
		tags=['Customer'],
		request_body=CustomerVehicleSerializer,
	)
	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = CustomerVehicleSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetVehicleInfoAPIView(APIView):
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
			logger.error(str(e), exc_info=True)
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

