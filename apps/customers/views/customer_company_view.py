from rest_framework import status
from rest_framework.generics import ListAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from apps.customers.models import CustomerCompany
from apps.customers.serializers import CompanyListSerializer
import logging


logger = logging.getLogger(__name__)


class CustomerCompanyListAPIView(ListAPIView):
	queryset = CustomerCompany.objects.filter(is_active=True).order_by('-created_at')
	serializer_class = CompanyListSerializer

	@swagger_auto_schema(
		tags=['Customer'],
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
				description='List of companies with id and name',
				schema=CompanyListSerializer(many=True)
			),
		}
	)
	def get(self, request, *args, **kwargs):
		paginated = request.query_params.get('paginated', 'true').lower() == 'true'
		if not paginated:
			self.pagination_class = None
		return self.list(request, *args, **kwargs)
