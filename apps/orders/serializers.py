from rest_framework import serializers
from .models import Order, OrderItem
from apps.products.models import ProductSKU


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

    def create(self, validated_data):
        items_data = validated_data.pop('item_orders')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('item_orders')
        instance.order_ref_number = validated_data.get('order_ref_number', instance.order_ref_number)
        instance.description = validated_data.get('description', instance.description)
        instance.current_route = validated_data.get('current_route', instance.current_route)
        instance.engineer = validated_data.get('engineer', instance.engineer)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.save()

        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                order_item = OrderItem.objects.get(id=item_id, order=instance)
                order_item.product_sku = item_data.get('product_sku', order_item.product_sku)
                order_item.price = item_data.get('price', order_item.price)
                order_item.quantity = item_data.get('quantity', order_item.quantity)
                order_item.discount = item_data.get('discount', order_item.discount)
                order_item.description = item_data.get('description', order_item.description)
                order_item.returned = item_data.get('returned', order_item.returned)
                order_item.credit_note = item_data.get('credit_note', order_item.credit_note)
                order_item.save()
            else:
                OrderItem.objects.create(order=instance, **item_data)

        return instance


class OrderItemReadSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product_sku', 'price', 'quantity', 'discount', 'description', 'returned',
                  'credit_note', 'total_price']

    def get_total_price(self, obj):
        return obj.total_price()


class OrderReadSerializer(serializers.ModelSerializer):
    item_orders = OrderItemReadSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'order_ref_number', 'description', 'current_route', 'engineer', 'customer', 'item_orders',
                  'total_price', 'total_quantity']

    def get_total_price(self, obj):
        return obj.total_price()

    def get_total_quantity(self, obj):
        return obj.total_quantity()

