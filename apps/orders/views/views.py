import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.accounts.models import Account
from apps.customers.models import CustomerVehicle
from apps.orders.models import Order, OrderItem, OrderOptionsData, OrderPaymentOptions
from apps.orders.serializers import OrderSerializer
from apps.products.models import ProductSKU

logger = logging.getLogger(__name__)


class OrderCreateAPIView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        request_body=OrderSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                description='Account created successfully',
                schema=serializer_class
            ),
        },
    )
    def post(self, request):
        try:
            data = request.data
            serializer = OrderSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            customer = data.get('customer')
            customer_vehicle_info = data.pop('customer_vehicle_info') if data.get('customer_vehicle_info') else None
            order_options = data.pop('order_options') if data.get('order_options') else None
            order_product_skus = data.pop('order_product_skus') if data.get('order_product_skus') else None
            payment_data = data.pop('payment_data') if data.get('payment_data') else None
            with transaction.atomic():
                vehicle = CustomerVehicle.objects.filter(
                    customer=customer,
                    vehicle_make=customer_vehicle_info.get('vehicle_make'),
                    vehicle_model=customer_vehicle_info.get('vehicle_model'),
                    vehicle_type=customer_vehicle_info.get('vehicle_type')
                ).first()
                if not vehicle:
                    raise ValidationError('Vehicle not found. but must provide customer vehicle info')
                data['vehicle'] = vehicle
                order = Order.objects.create(**data)
                if not order or not order_product_skus:
                    raise ValueError("Order and order_product_skus must be provided.")

                sku_codes = [item.get('sku_code') for item in order_product_skus]
                if not all(sku_codes):
                    raise ValueError("All items in order_product_skus must have a 'sku_code'.")

                product_skus = ProductSKU.objects.filter(sku_code__in=sku_codes)
                product_sku_map = {sku.sku_code: sku for sku in product_skus}
                missing_skus = set(sku_codes) - set(product_sku_map.keys())
                if missing_skus:
                    raise ObjectDoesNotExist(f"The following SKUs do not exist: {', '.join(missing_skus)}")

                bulks_skus_obj_list = []
                for item in order_product_skus:
                    sku_code = item.get('sku_code')
                    quantity = item.get('qty')
                    product_sku = product_sku_map.get(sku_code)

                    if not product_sku:
                        logger.warning(f"Skipping invalid SKU: {sku_code}")
                        continue
                    bulks_skus_obj_list.append(
                        OrderItem(
                            order=order,
                            product_sku=product_sku,
                            quantity=quantity,
                            price=product_sku.unit_price
                        )
                    )
                OrderItem.objects.bulk_create(bulks_skus_obj_list)

                OrderOptionsData.objects.create(
                        order=order,
                        existing_kit=order_options.get('existing_kit'),
                        available_date=order_options.get('available_date'),
                        service=order_options.get('service'),
                    )
                account_invoice = Account.objects.filter(id=payment_data.get('invoice_account_id')).first()
                OrderPaymentOptions.objects.create(
                    order=order,
                    invoice_account=account_invoice,
                    invoice_address=payment_data.get('invoice_address'),
                    # requested_by=payment_data.get('requested_by'),
                    po_number=payment_data.get('po_number'),
                )

            return Response(data={
                'message': "Order created successfully!",
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderUpdateAPIView(APIView):
    queryset = Order.objects.prefetch_related(
        Prefetch('item_orders', queryset=OrderItem.objects.all())
    ).all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        request_body=OrderSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='order updated successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        **OrderSerializer().data
                    }
                ),
            )
        }
    )
    def put(self, request, pk, *args, **kwargs):
        instance = Order.objects.filter(is_active=True, is_deleted=False).get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderRetrieveAPIView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related(
        Prefetch('item_orders', queryset=OrderItem.objects.all())
    ).all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Order retrieved successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        **OrderSerializer().data,
                    }
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.prefetch_related(
        Prefetch("item_orders", queryset=OrderItem.objects.filter(is_active=True)),
    ).order_by('-created_at')
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Order list',
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            **OrderSerializer().data,
                        }
                    )
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class OrderDestroyAPIView(DestroyAPIView):
    queryset = Order.objects.filter(is_active=True, is_deleted=False)
    lookup_field = 'pk'

    @swagger_auto_schema(
        tags=['Orders'],
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
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f'error on {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)
