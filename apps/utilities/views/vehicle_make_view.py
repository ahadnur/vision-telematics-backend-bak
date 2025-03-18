import logging
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.utilities.models import VehicleMake
from apps.utilities.serializers import VehicleMakeSerializer

logger = logging.getLogger(__name__)


class VehicleMakeCreateAPIView(CreateAPIView):
    queryset = VehicleMake.active_objects.all()
    serializer_class = VehicleMakeSerializer

    @swagger_auto_schema(
        tags=["Configuration"],
        request_body=VehicleMakeSerializer,
        responses={
            status.HTTP_201_CREATED: "Created Vehicle make successfully",
            status.HTTP_400_BAD_REQUEST: "Vehicle make with this name already exists!"
        }
    )
    def post(self, request, *args, **kwargs):
        make_name = request.data.get("make_name")

        existing_make = VehicleMake.objects.filter(make_name=make_name).first()

        if existing_make:
            if existing_make.is_deleted:
                existing_make.is_deleted = False
                existing_make.is_active = True
                existing_make.save()
                return Response(
                    VehicleMakeSerializer(existing_make).data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Vehicle make with this name already exists!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return super().post(request, *args, **kwargs)


class VehicleMakeListAPIView(ListAPIView):
	queryset = VehicleMake.active_objects.all()
	serializer_class = VehicleMakeSerializer

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
						"id": openapi.Schema(type=openapi.TYPE_INTEGER),
						"make_name": openapi.Schema(type=openapi.TYPE_STRING),
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


class VehicleMakeRetrieveAPIView(RetrieveAPIView):
	serializer_class = VehicleMakeSerializer
	queryset = VehicleMake.active_objects.all()

	@swagger_auto_schema(
		tags=["Configuration"],
		responses={
			status.HTTP_200_OK: openapi.Response(
				description="Vehicle make",
				schema=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						"id": openapi.Schema(type=openapi.TYPE_INTEGER),
						"make_name": openapi.Schema(type=openapi.TYPE_STRING),
					}
				)
			)
		}
	)
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)


class VehicleMakeUpdateAPIView(APIView):
    serializer_class = VehicleMakeSerializer

    @swagger_auto_schema(
        tags=["Configuration"],
        request_body=VehicleMakeSerializer,
        responses={
            status.HTTP_200_OK: "Vehicle make updated successfully!",
            status.HTTP_400_BAD_REQUEST: "Vehicle make with this name already exists!",
        }
    )
    def put(self, request, pk):
        try:
            instance = VehicleMake.active_objects.get(id=pk)
        except VehicleMake.DoesNotExist:
            return Response({"error": "Vehicle make not found"}, status=status.HTTP_404_NOT_FOUND)

        new_name = request.data.get("make_name")
        existing_make = VehicleMake.objects.filter(make_name=new_name).first()

        if existing_make:
            if existing_make.is_deleted:
                existing_make.is_deleted = False
                existing_make.is_active = True
                existing_make.save()
                return Response(
                    VehicleMakeSerializer(existing_make).data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Vehicle make with this name already exists!"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = VehicleMakeSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class VehicleMakeDeleteAPIView(DestroyAPIView):
	queryset = VehicleMake.active_objects.all()
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
