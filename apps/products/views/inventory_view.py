import logging

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.enums import OperationChoice
from apps.products.models import Inventory, StockMovement
from apps.products.serializers import InventorySerializer, StockMovementSerializer, UpdateStockMovementSerializer
from apps.products.helpers import InventoryService

logger = logging.getLogger(__name__)


class InventoryListAPIView(ListAPIView):
	queryset = Inventory.active_objects.all()
	serializer_class = InventorySerializer

	@swagger_auto_schema(
		tags=['Inventory'],
		responses={
			status.HTTP_200_OK: openapi.Schema(
				type=openapi.TYPE_ARRAY,
				items=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						**InventorySerializer().data
					}
				)
			),
			status.HTTP_400_BAD_REQUEST: "Bad Request",
			status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error"
		}
	)
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


class StockMovementListAPIView(ListAPIView):
	queryset = StockMovement.active_objects.all()
	serializer_class = StockMovementSerializer

	@swagger_auto_schema(
		tags=['Inventory'],
		responses={
			status.HTTP_200_OK: openapi.Schema(
				type=openapi.TYPE_ARRAY,
				items=openapi.Schema(
					type=openapi.TYPE_OBJECT,
					properties={
						**StockMovementSerializer().data
					}
				)
			),
			status.HTTP_400_BAD_REQUEST: "Bad Request",
			status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error"
		}
	)
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)


class UpdateStockAPIView(APIView):

	@swagger_auto_schema(
		tags=['Inventory'],
		request_body=UpdateStockMovementSerializer,
	)
	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UpdateStockMovementSerializer(data=data)
		if serializer.is_valid():
			product_sku = data.get('product_sku')
			quantity = int(data.get('quantity', 0))
			operation_type = data.get('operation_type')
			reason = data.get('reason')
			reference = data.get('reference')

			try:
				if operation_type == OperationChoice.ADD.value:
					InventoryService.add_stock(product_sku, quantity, reason, reference)
				elif operation_type == OperationChoice.REMOVE.value:
					InventoryService.remove_stock(product_sku, quantity, reason, reference)
				elif operation_type == OperationChoice.ADJUST.value:
					InventoryService.adjust_stock(product_sku, quantity, reason)
				else:
					return Response(
						{"detail": "Invalid operation type."},
						status=status.HTTP_400_BAD_REQUEST
					)
				return Response({"detail": "Stock updated successfully."}, status=status.HTTP_200_OK)
			except Exception as e:
				logger.error(e)
				return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
		else:
			logger.error(serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
