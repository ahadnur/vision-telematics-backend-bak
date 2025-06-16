import logging

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.orders.models import Order, OrderItem
from apps.products.models import ProductSKU

logger = logging.getLogger(__name__)


class OrderItemWriteSerializer(serializers.ModelSerializer):
    product_sku = serializers.PrimaryKeyRelatedField(queryset=ProductSKU.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_sku', 'price', 'quantity', 'discount', 'description', 'returned',
                  'credit_note']


class OrderWriteSerializer(serializers.ModelSerializer):
    item_orders = OrderItemWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_ref_number', 'description', 'current_route', 'engineer', 'customer', 'item_orders']

    def validate(self, data):
        try:
            items_data = data.get('item_orders', [])
            for item_data in items_data:
                product_sku_id = item_data.get('product_sku')
                quantity = item_data.get('quantity', 0)

                if product_sku_id and quantity > 0:
                    product_sku = ProductSKU.objects.get(pk=product_sku_id)
                    if quantity > product_sku.qty:
                        raise serializers.ValidationError(
                            f"Ordered quantity of {quantity} exceeds available stock for product SKU {product_sku_id}."
                        )
            return data
        except Exception as e:
            logger.error(e)
            raise serializers.ValidationError(e)

    def create(self, validated_data):
        items_data = validated_data.pop('item_orders')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            order_items = [
                OrderItem(order=order, **item_data) for item_data in items_data
            ]
            OrderItem.objects.bulk_create(order_items)

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('item_orders', [])

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        existing_item_ids = []
        new_items_data = []

        with transaction.atomic():
            for item_data in items_data:
                item_id = item_data.get('id')
                if item_id:
                    try:
                        order_item = OrderItem.objects.get(id=item_id, order=instance)
                    except OrderItem.DoesNotExist:
                        raise ValidationError(f"OrderItem with id {item_id} does not exist.")
                    for key, value in item_data.items():
                        setattr(order_item, key, value)
                    order_item.save()
                    existing_item_ids.append(item_id)
                else:
                    new_items_data.append(OrderItem(order=instance, **item_data))
            if new_items_data:
                OrderItem.objects.bulk_create(new_items_data)

            OrderItem.objects.filter(order=instance).exclude(id__in=existing_item_ids).delete()

        return instance


class OrderItemReadSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    product_sku = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_sku', 'price', 'quantity', 'discount', 'returned', 'total_price']

    @staticmethod
    def get_total_price(obj):
        return obj.total_price()

    @staticmethod
    def get_product_sku(obj):
        return obj.product_sku.sku_code


class OrderReadSerializer(serializers.ModelSerializer):
    item_orders = OrderItemReadSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_ref_number', 'description', 'current_route', 'engineer', 'customer', 'item_orders',
                  'total_price', 'total_quantity']

    @staticmethod
    def get_total_price(obj):
        return obj.total_price()

    @staticmethod
    def get_total_quantity(obj):
        return obj.total_quantity()

