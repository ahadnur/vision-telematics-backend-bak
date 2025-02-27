import logging

from django.db.models import F
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import DestroyAPIView

from apps.common.enums import OperationChoice
from apps.inventory.models import Inventory, StockMovement
from apps.inventory.serializers import InventorySerializer, InventoryCreateSerializer, StockMovementSerializer, UpdateStockMovementSerializer, InventoryUpdateSerializer, InventoryDestroySerializer
from apps.inventory.helpers import InventoryService

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
		return super().get(request, *args, **kwargs)


class InventoryCreateAPIView(CreateAPIView):
	queryset = Inventory.active_objects.all()
	serializer_class = InventoryCreateSerializer

	@swagger_auto_schema(
		tags=['Inventory'],
		request_body=InventoryCreateSerializer,
		responses={
			status.HTTP_201_CREATED: "Inventory Created",
			status.HTTP_400_BAD_REQUEST: "Bad Request",
			status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error"
		}
	)
	
	def post(self, request, *args, **kwargs):
		return super().post(request, *args, **kwargs)


class InventoryUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Inventory'],
        request_body=InventoryUpdateSerializer,
    )

    def put(self, request, pk=None, *args, **kwargs):
        serializer = InventoryUpdateSerializer(data=request.data)
        if serializer.is_valid():
            product_sku = serializer.validated_data['product_sku']
            quantity = serializer.validated_data['quantity']
            operation_type = serializer.validated_data['operation_type']
            reason = serializer.validated_data.get('reason')
            reference = serializer.validated_data.get('reference')

            try:
                if operation_type == OperationChoice.ADD.value:
                    InventoryService.add_stock(product_sku, quantity, reason, reference)
                elif operation_type == OperationChoice.REMOVE.value:
                    InventoryService.remove_stock(product_sku, quantity, reason, reference)
                elif operation_type == OperationChoice.ADJUST.value:
                    InventoryService.adjust_stock(product_sku, quantity, reason)
                else:
                    return Response({"detail": "Invalid operation type."}, status=status.HTTP_400_BAD_REQUEST)
                
                return Response({"detail": "Inventory updated successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(e)
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class InventoryDestroyAPIView(APIView):
    queryset = Inventory.active_objects.all()
    serializer_class = InventoryDestroySerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)
    
    def get_queryset(self):
        return self.queryset

    @swagger_auto_schema(
        tags=['Inventory'],
        request_body=InventoryDestroySerializer,
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_sku = serializer.validated_data['product_sku']

        try:
            instance = self.get_queryset().get(product_sku=product_sku)
        except Inventory.DoesNotExist:
            return Response({"detail": "Inventory not found."}, status=status.HTTP_404_NOT_FOUND)

        # Custom soft-delete logic
        instance.is_active = False 
        instance.is_deleted = True
        instance.save()

        return Response({"detail": "Inventory deleted successfully."}, status=status.HTTP_200_OK)



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
						# **StockMovementSerializer().data
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
