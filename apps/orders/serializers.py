import logging
from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product, ProductSKU
from apps.customers.serializers import CustomerOrderOptionsSerializer, CustomerVehicleInfoSerializer
from ..customers.models import Customer, CustomerInstallation, CustomerVehicleInfo

logger = logging.getLogger(__name__)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product_sku', 'quantity']


class CreateOrderSerializer(serializers.ModelSerializer):
    customer_order_options = CustomerOrderOptionsSerializer()
    customer_vehicle_info = CustomerVehicleInfoSerializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'items', 'customer_order_options', 'customer_vehicle_info', 'created_by']

    def create(self, validated_data):
        customer_order_data = validated_data.pop('customer_order_options')
        customer_vehicle_data = validated_data.pop('customer_vehicle_info')
        items_data = validated_data.pop('items')

        try:
            with transaction.atomic():
                customer_options = CustomerInstallation.objects.create(**customer_order_data)
                customer_vehicle_info = CustomerVehicleInfo.objects.create(**customer_vehicle_data)
                order = Order.objects.create(
                    customer=validated_data.get('customer'),
                    created_by=validated_data.get('created_by')  # Assuming `created_by` is provided
                )
                for item_data in items_data:
                    product_sku = item_data.get('product_sku')
                    quantity = item_data.get('quantity')
                    product_sku = ProductSKU.objects.get(id=product_sku.id)
                    OrderItem.objects.create(
                        order=order,
                        product_sku=product_sku,
                        quantity=quantity,
                        price=product_sku.unit_price
                    )
                return {
                    'customer_order_option': customer_options,
                    'customer_vehicle_info': customer_vehicle_info,
                    'order': order
                }
        except Exception as e:
            logger.error(str(e), exc_info=True)
            raise serializers.ValidationError(str(e))