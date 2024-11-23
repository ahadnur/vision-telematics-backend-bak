from rest_framework.generics import ListAPIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.customers.schemas import customer_dropdown_response_schema
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
			status.HTTP_200_OK: customer_dropdown_response_schema
		}
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)
