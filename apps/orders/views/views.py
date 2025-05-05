import logging

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from apps.accounts.models import Account
from apps.customers.models import CustomerVehicle
from apps.orders.models import Order, OrderItem, OrderOptionsData, OrderPaymentOptions, Booking, CustomerInvoice
from apps.orders.serializers import OrderSerializer, OptionDataSerializer, PaymentDataSerializer
from apps.orders.swagger_schema import order_list_schema
from apps.products.models import ProductSKU
from apps.common.enums import OrderItemStatusChoice, OrderStatusChoice, OperationChoice
from apps.inventory.models import Inventory

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
            customer_vehicle_info = data.pop('vehicle') if data.get('vehicle') else None
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
    @swagger_auto_schema(
        tags=['Orders'],
        request_body=OrderSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Order updated successfully",
                schema=OrderSerializer() 
            ),
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal Server Error",
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            order = get_object_or_404(Order, pk=pk, is_active=True, is_deleted=False)
            data = request.data

            serializer = OrderSerializer(order, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            with transaction.atomic():
                order = serializer.save()

                # Update order options data 
                if 'order_options' in data:
                    options_data = data['order_options']
                    
                    if hasattr(order, 'options_data'):
                        options_serializer = OptionDataSerializer(
                            order.options_data,
                            data=options_data,
                            partial=True
                        )
                        options_serializer.is_valid(raise_exception=True)
                        options_serializer.save()
                    else:
                        OrderOptionsData.objects.create(order=order, **options_data)

                # Update payment data 
                if 'payment_data' in data:
                    payment_data = data['payment_data']
                    
                    payment_instance = OrderPaymentOptions.objects.filter(order=order).first()
                    if payment_instance:
                        payment_serializer = PaymentDataSerializer(
                            payment_instance,
                            data=payment_data,
                            partial=True
                        )
                        payment_serializer.is_valid(raise_exception=True)
                        payment_serializer.save()
                    else:
                        OrderPaymentOptions.objects.create(order=order, **payment_data)

                # Update order item
                if 'order_product_skus' in data:
                    sku_data_list = data['order_product_skus']
                    existing_item_ids = []
                    
                    for sku_data in sku_data_list:
                        
                        item_id = sku_data.get('id')
                        if item_id:
                            try:
                                order_item = OrderItem.objects.get(id=item_id, order=order)
                            except OrderItem.DoesNotExist:
                                raise ValidationError(
                                    f"OrderItem with id {item_id} does not exist for this order."
                                )
                                
                            for field in ['quantity', 'price', 'discount']:
                                if field in sku_data:
                                    setattr(order_item, field, sku_data[field])
                            order_item.save()
                            existing_item_ids.append(order_item.id)
                        else:
                            # Create new OrderItem using the provided SKU code and quantity.
                            sku_code = sku_data.get('sku_code')
                            quantity = sku_data.get('qty', 0)
                            if not sku_code:
                                raise ValidationError("SKU code must be provided for new items.")
                            try:
                                product_sku = ProductSKU.objects.get(sku_code=sku_code)
                            except ProductSKU.DoesNotExist:
                                raise ValidationError(
                                    f"Product SKU with code {sku_code} does not exist."
                                )
                            new_item = OrderItem.objects.create(
                                order=order,
                                product_sku=product_sku,
                                quantity=quantity,
                                price=product_sku.unit_price, 
                                discount=sku_data.get('discount', None)
                            )
                            existing_item_ids.append(new_item.id)
                    
                    # OrderItem.objects.filter(order=order).exclude(id__in=existing_item_ids).delete()

            updated_serializer = OrderSerializer(order)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error updating order: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OrderRetrieveAPIView(RetrieveAPIView):
    queryset = Order.objects.filter(is_deleted=False, is_active=True).prefetch_related(
        Prefetch('item_orders', queryset=OrderItem.objects.all())
    ).all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        responses= {
            status.HTTP_200_OK: order_list_schema
        }
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.filter(is_deleted=False, is_active=True).prefetch_related(
        Prefetch("item_orders", queryset=OrderItem.objects.filter(is_active=True)),
    ).order_by('-created_at')
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        tags=['Orders'],
        responses={
            status.HTTP_200_OK: order_list_schema
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
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error(f'error on {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)



class OrderStatusChangeAPIView(APIView):
    @swagger_auto_schema(
        tags=['Orders'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['new_status'],
            properties={
                'new_status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=[choice[0] for choice in OrderStatusChoice.choices],
                    description='New status for the order'
                )
            }
        ),
        responses={
            status.HTTP_200_OK: "Order status updated successfully",
            status.HTTP_400_BAD_REQUEST: "Bad Request",
            status.HTTP_404_NOT_FOUND: "Order not found"
        }
    )
    def put(self, request, pk, *args, **kwargs):
        try:
            order = Order.objects.prefetch_related('item_orders').get(pk=pk, is_active=True, is_deleted=False)
        except Order.DoesNotExist:
            return Response({'error' : 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('new_status')
        valid_statuses = [choice[0] for choice in OrderStatusChoice.choices]

        if not new_status or new_status not in valid_statuses:
            return Response({'error' : f'Invalid status, valid: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)

        old_status = order.order_status

        try:
            with transaction.atomic():
                if new_status == OrderStatusChoice.CREATED:
                    return Response({"error" : f"You cannot reasign status to: {new_status}"}, status.HTTP_400_BAD_REQUEST)
                elif old_status == OrderStatusChoice.REJECTED:
                    return Response({"error" : f"Order is already rejected!"}, status.HTTP_400_BAD_REQUEST)
                elif old_status == OrderStatusChoice.DELIVERED:
                    return Response({"error": f"Order is already completed!"}, status.HTTP_400_BAD_REQUEST)
                elif old_status == new_status:
                    return Response({"error" :f"Order is already in {new_status} state!"}, status.HTTP_400_BAD_REQUEST)
                    
                elif new_status == OrderStatusChoice.PROCESSING and old_status != OrderStatusChoice.PROCESSING:
                    self.handle_processing_transition(order)
                elif new_status == OrderStatusChoice.REJECTED and old_status == OrderStatusChoice.PROCESSING:
                    self.handle_rejection_from_processing(order)
                elif new_status == OrderStatusChoice.DELIVERED and old_status == OrderStatusChoice.PROCESSING:
                    self.handle_delivered_transition(order)
                
                self.update_bookings(order, new_status)

                # Update order status
                order.order_status = new_status
                order.save()


                return Response({'message': 'Order status updated successfully'}, status=status.HTTP_200_OK)
                
        except ValidationError as e:
            return Response({'error' : f'error: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error updating order status: {str(e)}")
            return Response(
                {'error': 'Internal server error'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    def handle_processing_transition(self, order):
        if hasattr(order, 'customer_invoice'):
            raise ValidationError(f"Invoice already exists for order {order.order_ref_number}")

        for item in order.item_orders.all():
            product_sku = item.product_sku
            if product_sku.qty < item.quantity:
                raise ValidationError(
                    f'Insufficient stock for {product_sku.sku_code}. '
                    f'Available: {product_sku.qty}, Required: {item.quantity}'
                )
            product_sku.qty -= item.quantity
            product_sku.save()
            item.status = OrderItemStatusChoice.SHIPPED
            item.save()
        
        CustomerInvoice.objects.create(
            shipping_charge=order.shipping_charge or 0.0,
            total_discount=order.total_discount or 0.0,
            order=order,
            invoice_number=f"CINV-{order.order_ref_number}-{now().strftime('%Y%m%d%H%M%S')}",
            subtotal=order.total_price(),
            total_amount=order.total_price() - (order.total_discount or 0.0),
            payment_status=order.customer_payment_status,
            billing_address=order.billing_address,
            shipping_address=order.shipping_address,
        )


    def handle_rejection_from_processing(self, order):
        for item in order.item_orders.all():
            product_sku = item.product_sku
            product_sku.qty += item.quantity
            product_sku.save()
            item.status = OrderItemStatusChoice.REJECTED
            item.save()

    def update_bookings(self, order, new_status):
        bookings = Booking.objects.filter(order=order)
        if not bookings.exists():
            return

        if new_status == OrderStatusChoice.PROCESSING:
            bookings.update(booking_status='in_progress')
        elif new_status == OrderStatusChoice.DELIVERED:
            bookings.update(booking_status='completed')
        elif new_status == OrderStatusChoice.REJECTED:
            bookings.update(booking_status='cancelled')

    def handle_delivered_transition(self, order):
        # Order -> OrderItem:
        # Each order has one or more OrderItem instances.

        # OrderItem -> ProductSKU:
        # Each OrderItem references a ProductSKU (via the product_sku foreign key).

        # ProductSKU -> Inventory:
        # The Inventory model also references ProductSKU (via its product_sku foreign key).

        for item in order.item_orders.all():
            try:
                inventory = Inventory.objects.get(product_sku=item.product_sku)
            except Inventory.DoesNotExist:
                raise ValidationError(
                    f"Inventory record not found for SKU: {item.product_sku.sku_code}"
                )
            
            if inventory.stock_quantity < item.quantity:
                raise ValidationError(
                    f"Insufficient stock for SKU: {item.product_sku.sku_code}. "
                    f"Available: {inventory.stock_quantity}, Required: {item.quantity}"
                )
            
            inventory.update_stock(
                quantity=item.quantity,
                operation_type= OperationChoice.REMOVE.value,
                reason="Order Delivered",
                reference= order.order_ref_number
            )
            item.status = OrderItemStatusChoice.DELIVERED
            item.save()
