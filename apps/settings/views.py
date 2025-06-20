import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.settings.models import InstallType
from apps.settings.serializers import InstallTypeSerializer

logger = logging.getLogger(__name__)

class InstallTypeCreateAPIView(CreateAPIView):
	queryset = InstallType.objects.filter(is_active=True, is_deleted=False)
	serializer_class = InstallTypeSerializer

	@swagger_auto_schema(
		tags=['Settings'],
		request_body=InstallTypeSerializer,
		responses={
			status.HTTP_201_CREATED: openapi.Response(
				description='Created Install type',
				schema=InstallTypeSerializer
			)
		}
	)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class InstallTypeUpdateAPIView(APIView):
	serializer_class = InstallTypeSerializer

	@swagger_auto_schema(
		tags=['Settings'],
		request_body=InstallTypeSerializer,
		responses={
			status.HTTP_200_OK: openapi.Response(
				description='Updated Install type',
				schema=InstallTypeSerializer
			)
		}
	)
	def put(self, request, pk):
		try:
			instance = InstallType.active_objects.get(id=pk)
		except InstallType.DoesNotExist:
			return Response({"error": "InstallType not found"}, status=status.HTTP_404_NOT_FOUND)

		serializer = InstallTypeSerializer(instance=instance, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_200_OK)


class InstallTypeListAPIView(ListAPIView):
	queryset = InstallType.objects.filter(is_active=True).order_by('-created_at')
	serializer_class = InstallTypeSerializer

	@swagger_auto_schema(
		tags=['Settings'],
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
	)
	def get(self, request, *args, **kwargs):
		paginated = request.query_params.get('paginated', 'true').lower() == 'true'
		if not paginated:
			self.pagination_class = None
		return self.list(request, *args, **kwargs)


class InstallTypeDeleteAPIView(DestroyAPIView):
	serializer_class = InstallTypeSerializer
	queryset = InstallType.active_objects.all()

	@swagger_auto_schema(
		tags=['Settings'],
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
