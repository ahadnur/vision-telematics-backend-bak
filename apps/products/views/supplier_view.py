import logging

from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response

from apps.products.models import Supplier
from apps.products.schemas.supplier_schema import supplier_response_schema, supplier_manual_parameter
from apps.products.serializers import SupplierSerializer

logger = logging.getLogger(__name__)


class SupplierListAPIView(ListAPIView):
	serializer_class = SupplierSerializer

	def get_queryset(self):
		return Supplier.objects.filter(is_active=True)

	@swagger_auto_schema(
		tags=['Suppliers'],
		manual_parameters=[
			supplier_manual_parameter
		],
		responses={
			status.HTTP_200_OK: supplier_response_schema,
			status.HTTP_400_BAD_REQUEST: "Bad Request",
			status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error"
		}
	)
	def get(self, request, *args, **kwargs):
		paginated = request.query_params.get('paginated', 'true').lower() == 'true'
		if not paginated:
			self.pagination_class = None
		return self.list(request, *args, **kwargs)


class SupplierCreateAPIView(CreateAPIView):
	queryset = Supplier.active_objects.all()
	serializer_class = SupplierSerializer

	@swagger_auto_schema(
		tags=['Suppliers'],
		operation_description="Create a new supplier",
		request_body=SupplierSerializer(),
		responses={
			status.HTTP_201_CREATED: "Successfully created!",
			status.HTTP_400_BAD_REQUEST: "Bad Request",
			status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error"
		},
	)
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)


class SupplierDetailAPIView(RetrieveAPIView):
	queryset = Supplier.active_objects.all()
	serializer_class = SupplierSerializer

	@swagger_auto_schema(
		tags=['Suppliers'],
		operation_description="Retrieve details of a specific supplier",
		responses={
			status.HTTP_200_OK: supplier_response_schema,
			status.HTTP_400_BAD_REQUEST: "Bad Request",
			status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error"
		},
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)


class SupplierUpdateAPIView(UpdateAPIView):
	http_method_names = ['put']
	queryset = Supplier.active_objects.all()
	serializer_class = SupplierSerializer

	@swagger_auto_schema(
		tags=['Suppliers'],
		operation_description="Update details of a specific supplier",
		request_body=SupplierSerializer(),
		responses={
			status.HTTP_200_OK: "Successfully updated!",
			status.HTTP_400_BAD_REQUEST: "Bad Request",
			status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error"
		},
	)
	def put(self, request, *args, **kwargs):
		return super().put(request, *args, **kwargs)


class SupplierDeleteAPIView(DestroyAPIView):
	queryset = Supplier.objects.all()
	serializer_class = SupplierSerializer

	@swagger_auto_schema(
		tags=['Suppliers'],
		operation_description="Delete a supplier by ID",
		responses={
			status.HTTP_200_OK: "Successfully deleted!",
			status.HTTP_404_NOT_FOUND: "Supplier not found!",
			status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error!"
		},
	)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

	def destroy(self, request, *args, **kwargs):
		try:
			instance = self.get_object()
			instance.is_active = False
			instance.is_deleted = True
			instance.save()
			return Response(status=status.HTTP_204_NO_CONTENT)
		except Supplier.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
			logger.error(str(e))
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



