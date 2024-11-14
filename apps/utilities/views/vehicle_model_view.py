import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.utilities.models import VehicleModel
from apps.utilities.serializers import VehicleModelSerializer

logger = logging.getLogger(__name__)


class VehicleModelCreateAPIView(CreateAPIView):
	queryset = VehicleModel.active_objects.all()
	serializer_class = VehicleModelSerializer

	@swagger_auto_schema(
		tags=["Configuration"],
		request_body=VehicleModelSerializer,
		responses={
			status.HTTP_201_CREATED: "Created Vehicle Type successfully",
		}
	)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class VehicleModelListAPIView(ListAPIView):
	queryset = VehicleModel.active_objects.all()
	serializer_class = VehicleModelSerializer
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
				description="List of Vehicle Model",
				schema=openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=openapi.Schema(
						type=openapi.TYPE_OBJECT,
						properties={
							**VehicleModelSerializer().data,
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


class VehicleModelRetrieveAPIView(RetrieveAPIView):
	serializer_class = VehicleModelSerializer
	queryset = VehicleModel.active_objects.all()

	@swagger_auto_schema(
		tags=["Configuration"],
		responses={
			status.HTTP_200_OK: openapi.Response(
				description="Vehicle Type",
				schema=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						**VehicleModelSerializer().data,
					}
				)
			)
		}
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class VehicleModelUpdateAPIView(APIView):
	serializer_class = VehicleModelSerializer

	@swagger_auto_schema(
		tags=["Configuration"],
		request_body=VehicleModelSerializer,
		responses={
			status.HTTP_200_OK: openapi.Response(
				description="Vehicle Type",
				schema=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						**VehicleModelSerializer().data,
					}
				)
			)
		}
	)
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def update(self, request, pk):
		try:
			instance = VehicleModel.objects.filter(id=pk, is_active=True).first()
			serializer = self.serializer_class(instance, data=request.data)
			serializer.is_valid(raise_exception=True)
			serializer.save()
			return Response(status=status.HTTP_200_OK)
		except Exception as e:
			logger.error(e)
			return Response(status=status.HTTP_400_BAD_REQUEST)


class VehicleModelDeleteAPIView(DestroyAPIView):
	queryset = VehicleModel.active_objects.all()
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
			instance.save()
			return Response(status=status.HTTP_204_NO_CONTENT)
		except Exception as e:
			logger.error(f'error on {e}')
			return Response(status=status.HTTP_400_BAD_REQUEST)
