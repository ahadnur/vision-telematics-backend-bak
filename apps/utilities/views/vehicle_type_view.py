import logging


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.utilities.models import VehicleType
from apps.utilities.serializers.vehicle_type_serializer import VehicleTypeSerializer

logger = logging.getLogger(__name__)


class VehicleTypeCreateAPIView(CreateAPIView):
	queryset = VehicleType.objects.all()
	serializer_class = VehicleTypeSerializer

	@swagger_auto_schema(
		tags=["Configuration"],
		request_body=VehicleTypeSerializer,
		responses={
			status.HTTP_201_CREATED: "Created Vehicle Type successfully",
		}
	)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class VehicleTypeListAPIView(ListAPIView):
	queryset = VehicleType.objects.all()
	serializer_class = VehicleTypeSerializer
	pagination_class = None

	@swagger_auto_schema(
		tags=["Configuration"],
		manual_parameters=[
			openapi.Parameter(
				'paginated',
				openapi.IN_QUERY,
				description="Enable or disable pagination (true or false)",
				type=openapi.TYPE_BOOLEAN,
				required=False,
				default=True
			)
		],
		responses={
			status.HTTP_200_OK: openapi.Response(
				description="List of Vehicle Types",
				schema=openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=openapi.Schema(
						type=openapi.TYPE_OBJECT,
						properties={
							**VehicleTypeSerializer().data,
						}
					)
				)
			)
		}
	)
	def get(self, request, *args, **kwargs):
		paginated = request.query_params.get('paginated', 'true').lower() == 'true'
		if not paginated:
			self.pagination_class = None
		return self.list(request, *args, **kwargs)


class VehicleTypeRetrieveAPIView(RetrieveAPIView):
	serializer_class = VehicleTypeSerializer
	queryset = VehicleType.objects.filter(is_active=True)

	@swagger_auto_schema(
		tags=["Configuration"],
		responses={
			status.HTTP_200_OK: openapi.Response(
				description="Vehicle Type",
				schema=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						**VehicleTypeSerializer().data,
					}
				)
			)
		}
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class VehicleTypeUpdateAPIView(APIView):
	serializer_class = VehicleTypeSerializer

	@swagger_auto_schema(
		tags=["Configuration"],
		request_body=VehicleTypeSerializer,
		responses={
			status.HTTP_200_OK: openapi.Response(
				description="Vehicle Type",
				schema=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						**VehicleTypeSerializer().data,
					}
				)
			)
		}
	)
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def update(self, request, pk):
		try:
			instance = VehicleType.objects.filter(id=pk, is_active=True)
			serializer = self.serializer_class(instance, data=request.data)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(status=status.HTTP_200_OK)
		except Exception as e:
			logger.error(e)
			return Response(status=status.HTTP_400_BAD_REQUEST)


class VehicleTypeDeleteAPIView(DestroyAPIView):
	queryset = VehicleType.objects.filter(is_active=True, is_deleted=False)
	lookup_field = 'pk'

	@swagger_auto_schema(
		tags=['Configuration'],
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
			return Response(status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			logger.error(f'error on {e}')
			return Response(status=status.HTTP_400_BAD_REQUEST)
