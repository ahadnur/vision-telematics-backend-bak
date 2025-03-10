import logging

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.accounts.models import Account
from apps.customers.models import CustomerVehicle
from apps.orders.models import (
    Order, 
    OrderItem, 
    OrderOptionsData, 
    OrderPaymentOptions, 
    Booking, 
    OrderRefund, 
    ReturnItem
)
from apps.orders.serializers import (
    OrderSerializer, 
    OptionDataSerializer, 
    PaymentDataSerializer, 

    OrderReturnDetailSerializer,
    OrderReturnCreateSerializer,
    OrderReturnUpdateSerializer,
    
    OrderRefundSerializer,
    OrderRefundCreateSerializer,
    OrderRefundUpdateSerializer,
)
from apps.orders.swagger_schema import order_return_schema
from apps.products.models import ProductSKU
from apps.common.enums import ReturnStatusType, ShipmentMode
from apps.inventory.models import Inventory

logger = logging.getLogger(__name__)


class OrderReturnListAPIView(ListAPIView):
    queryset = ReturnItem.objects.filter(is_deleted=False, is_active=True).select_related(
        'order_refund', 'order_item', 'order_item__order', 'order_item__product_sku'
    ).order_by('-created_at')
    serializer_class = OrderReturnDetailSerializer

    @swagger_auto_schema(
        tags=['Return & Refund'],
        responses={
            status.HTTP_200_OK: order_return_schema
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderReturnCreateAPIView(CreateAPIView):
    serializer_class = OrderReturnCreateSerializer
    queryset = ReturnItem.objects.all()

    def perform_create(self, serializer):
        order_item = serializer.validated_data['order_item']
        order = order_item.order
        order_refund, created = OrderRefund.objects.get_or_create(order=order)
        serializer.save(order_refund=order_refund)

    @swagger_auto_schema(
        tags=['Return & Refund'],
        request_body=OrderReturnCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Order return created successfully',
                schema=OrderReturnCreateSerializer
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrderReturnUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Return & Refund'],
        request_body=OrderReturnUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Order return updated successfully",
                schema=OrderReturnUpdateSerializer()
            ),
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            return_item = get_object_or_404(ReturnItem, pk=pk, is_active=True, is_deleted=False)
            serializer = OrderReturnUpdateSerializer(return_item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data

            old_status = return_item.return_status
            new_status = validated_data.get('return_status', old_status)
            is_restocked = validated_data.get('is_restocked', False)

            with transaction.atomic():
                if return_item.return_status in [ReturnStatusType.APPROVED, ReturnStatusType.COMPLETED]:
                    restricted_fields = ['quantity', 'order_item']
                    for field in restricted_fields:
                        if field in request.data:
                            raise ValidationError({field: f"Cannot modify {field} after approval or completion."})

                if new_status != old_status:
                    if new_status == ReturnStatusType.REJECTED:
                        return_rejected_reason = request.data.get('return_rejected_reason')
                        if not return_rejected_reason:
                            raise ValidationError({'return_rejected_reason': 'Required when rejecting.'})
                        return_item.return_rejected_reason = return_rejected_reason
                        return_item.return_rejected_by = request.user.username
                    elif new_status == ReturnStatusType.COMPLETED and is_restocked:
                        order_item = return_item.order_item
                        product_sku = order_item.product_sku
                        quantity = return_item.quantity

                        product_sku.qty += quantity
                        product_sku.save()

                        try:
                            inventory = Inventory.objects.get(product_sku=product_sku)
                        except Inventory.DoesNotExist:
                            raise ValidationError(f"Inventory not found for SKU {product_sku.sku_code}")

                        inventory.update_stock(
                            quantity=quantity,
                            operation_type=OperationChoice.ADD,
                            reason=f"ReturnItem {return_item.id} restock",
                            reference=return_item.order_refund.order.order_ref_number
                        )

                        return_item.restocked_at = timezone.now()
                        order_item.returned = True
                        order_item.order_refund.refund_completed = timezone.now()
                        order_item.save()

                for attr, value in validated_data.items():
                    setattr(return_item, attr, value)
                return_item.save()

                if new_status == ReturnStatusType.APPROVED:
                    order_refund = return_item.order_refund
                    if not order_refund.refund_initiated:
                        order_refund.refund_initiated = timezone.now()
                        order_refund.save()

                return Response(OrderReturnSerializer(return_item).data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Update error: {e}")
            return Response({'error': 'Internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderReturnRetrieveAPIView(RetrieveAPIView):
    queryset = ReturnItem.objects.filter(is_deleted=False, is_active=True).select_related(
        'order_refund', 'order_item', 'order_item__order', 'order_item__product_sku'
    )
    serializer_class = OrderReturnDetailSerializer

    @swagger_auto_schema(
        tags=['Return & Refund'],
        responses={status.HTTP_200_OK: order_return_schema}
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderReturnDestroyAPIView(DestroyAPIView):
    queryset = ReturnItem.objects.filter(is_active=True, is_deleted=False)
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Return & Refund'],
        responses={
            status.HTTP_204_NO_CONTENT: "Successfully deleted!",
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            order_refund = instance.order_refund
            
            instance.is_deleted = True
            instance.is_active = False
            instance.save()

            active_returns_exist = ReturnItem.objects.filter(
                order_refund=order_refund,
                is_deleted=False,
                is_active=True
            ).exists()

            if not active_returns_exist:
                order_refund.is_deleted = True
                order_refund.is_active = False
                order_refund.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderRefundListAPIView(ListAPIView):
    queryset = OrderRefund.objects.filter(is_active=True, is_deleted=False) \
        .select_related('order') \
        .prefetch_related('return_items') \
        .order_by('-created_at')
    serializer_class = OrderRefundSerializer

    @swagger_auto_schema(
        tags=['Return & Refund'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="List of Order Refunds",
                schema=OrderRefundSerializer(many=True)
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class OrderRefundRetrieveAPIView(RetrieveAPIView):
    queryset = OrderRefund.objects.filter(is_active=True, is_deleted=False) \
        .select_related('order') \
        .prefetch_related('return_items')
    serializer_class = OrderRefundSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Return & Refund'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Refund details",
                schema=OrderRefundSerializer
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class OrderRefundCreateAPIView(CreateAPIView):
    serializer_class = OrderRefundCreateSerializer
    queryset = OrderRefund.objects.all()

    @swagger_auto_schema(
        tags=['Return & Refund'],
        request_body=OrderRefundCreateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description="Order Refund created successfully",
                schema=OrderRefundSerializer
            )
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class OrderRefundUpdateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Return & Refund'],
        request_body=OrderRefundUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Order Refund updated successfully",
                schema=OrderRefundSerializer()
            ),
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            refund_instance = get_object_or_404(OrderRefund, pk=pk, is_active=True, is_deleted=False)
            serializer = OrderRefundUpdateSerializer(refund_instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                serializer.save()
            updated_serializer = OrderRefundSerializer(refund_instance)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"OrderRefund update error (pk={pk}): {e}")
            return Response({'error': 'Internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderRefundDestroyAPIView(DestroyAPIView):
    queryset = OrderRefund.objects.filter(is_active=True, is_deleted=False)
    serializer_class = OrderRefundSerializer
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Return & Refund'],
        responses={
            status.HTTP_204_NO_CONTENT: "Successfully deleted!",
        }
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            refund_instance = self.get_object()
            refund_instance.is_active = False
            refund_instance.is_deleted = True
            refund_instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)