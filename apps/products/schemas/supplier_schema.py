from drf_yasg import openapi

from apps.products.serializers import SupplierSerializer

supplier_response_schema = openapi.Schema(
	type=openapi.TYPE_ARRAY,
	items=openapi.Schema(
		type=openapi.TYPE_OBJECT,
		properties={
			**SupplierSerializer().data
		}
	)
)

supplier_manual_parameter = openapi.Parameter(
	'paginated',
	openapi.IN_QUERY,
	description="Enable or disable pagination (true or false)",
	type=openapi.TYPE_BOOLEAN,
	required=False,
	default=True
)
