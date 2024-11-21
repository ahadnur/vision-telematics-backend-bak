from rest_framework.generics import ListAPIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.customers.serializers import CustomerDropdownSerializer
from apps.customers.models import Customer


class CustomerDropdownListAPIView(ListAPIView):
	serializer_class = CustomerDropdownSerializer
	queryset = Customer.active_objects.all()
	pagination_class = None

	@swagger_auto_schema(
		tags=['Customer'],
		operation_summary="Retrieve Customer Dropdown List",
		operation_description="Returns a list of active customer IDs and names for dropdowns or selection components.",
		responses={
			status.HTTP_200_OK: openapi.Response(
				description="List of customer IDs and names",
				schema=openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=openapi.Schema(
						type=openapi.TYPE_OBJECT,
						properties={
							"id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Customer ID"),
							"name": openapi.Schema(type=openapi.TYPE_STRING, description="Customer Name"),
						}
					)
				)
			)
		}
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)
