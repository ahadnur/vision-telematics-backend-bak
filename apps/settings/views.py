from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from apps.settings.models import InstallType
from apps.settings.serializers import InstallTypeSerializer


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


class InstallTypeUpdateAPIView(UpdateAPIView):
	queryset = InstallType.objects.filter(is_active=True, is_deleted=False)
	serializer_class = InstallTypeSerializer
	lookup_field = 'pk'

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
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)


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
