from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import Product, ProductSKU


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


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['created_at', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

