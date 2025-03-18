import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.utilities.models import VehicleModel
from apps.utilities.serializers import VehicleModelSerializer
from apps.utilities.swagger_schema import vehicle_model_schema

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
        name = request.data.get("name")
        vehicle_make_id = request.data.get("vehicle_make")

        existing_model = VehicleModel.objects.filter(name=name, is_deleted=True, is_active=False).first()

        if existing_model:
            existing_model.vehicle_make_id = vehicle_make_id
            existing_model.is_deleted = False
            existing_model.is_active = True
            existing_model.save()
            return Response(
                VehicleModelSerializer(existing_model).data,
                status=status.HTTP_200_OK
            )

        return super().post(request, *args, **kwargs)



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
			status.HTTP_200_OK: vehicle_model_schema,
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
			status.HTTP_200_OK: vehicle_model_schema,
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
            status.HTTP_200_OK: vehicle_model_schema
        }
    )
    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk)

    def update(self, request, pk):
        try:
            instance = VehicleModel.active_objects.get(id=pk)
            serializer = self.serializer_class(instance, data=request.data, partial=True)
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
