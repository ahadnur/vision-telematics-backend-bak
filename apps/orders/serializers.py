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
        fields = ['product_sku', 'quantity', 'total_price']

    def validate_quantity(self, value):
        # Validate that the ordered quantity doesn't exceed the SKU quantity
        sku = self.instance.product_sku if self.instance else self.initial_data['product_sku']
        product_sku = ProductSKU.objects.get(pk=sku)
        if value > product_sku.qty:
            raise serializers.ValidationError("Ordered quantity exceeds available stock.")
        return value


class CreateOrderSerializer(serializers.ModelSerializer):
    customer_order_options = CustomerOrderOptionsSerializer()
    customer_vehicle_info = CustomerVehicleInfoSerializer()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['created_at', 'items', 'customer_order_options', 'customer_vehicle_info']

    def create(self, validated_data):
        customer_order_data = validated_data.pop('customer_order_options')
        customer_vehicle_data = validated_data.pop('customer_vehicle_info')
        items_data = validated_data.pop('items')
        try:
            with transaction.atomic():
                customer_options = CustomerInstallation.objects.create(
                    CustomerOrderOptionsSerializer(),
                    validated_data=customer_order_data,
                )
                customer_vehicle_info = CustomerVehicleInfo.objects.create(
                    CustomerVehicleInfoSerializer(),
                    customer_vehicle_data=customer_vehicle_data,
                )
                order = Order.objects.create(**validated_data)
                for item_data in items_data:
                    OrderItem.objects.create(order=order, **item_data)

                return {
                    'customer_order_option': customer_options,
                    'customer_vehicle_info': customer_vehicle_info,
                }
        except Exception as e:
            logger.error(str(e), exc_info=True)
            raise serializers.ValidationError(str(e))
