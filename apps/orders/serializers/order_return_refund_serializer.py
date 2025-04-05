from rest_framework import serializers

from apps.orders.models import ReturnItem, OrderRefund
from apps.orders.serializers import OrderSerializer
from apps.products.serializers import ProductSKUSerializer



class OrderReturnDetailSerializer(serializers.ModelSerializer):
    order = OrderSerializer(source='order_item.order', read_only=True)
    product = ProductSKUSerializer(source='order_item.product_sku', read_only=True)

    class Meta:
        model = ReturnItem
        fields = [
            'id',
            'order',
            'product',
            'order_item',
            'quantity',
            'return_status',
            'refund_amount',
            'pickup_address',
            'drop_off_address',
            'reason',
            'shipment_mode',
            'cancellation_charges',
            'return_rejected_reason',
            'return_rejected_by',
            'notes',
            'is_restocked',
            'restocked_at',
        ]

class OrderReturnCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnItem
        fields = [
            'order_item',
            'quantity',
            'pickup_address',
            'drop_off_address',
            'reason',
            'shipment_mode',
            'cancellation_charges',
            'notes',
        ]

    def validate(self, data):
        order_item = data['order_item']
        return_quantity = data['quantity']

        if return_quantity > order_item.quantity:
            raise serializers.ValidationError("Return quantity exceeds original order quantity.")

        return data


class OrderReturnUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnItem
        fields = [
            'order_refund',
            'order_item',
            'quantity',
            'return_status',
            'pickup_address',
            'drop_off_address',
            'reason',
            'shipment_mode',
            'cancellation_charges',
            'return_rejected_reason',
            'return_rejected_by',
            'notes',
            'is_restocked',
            'restocked_at',
        ]
        read_only = ['order_refund', 'order_item', 'quantity', 'restocked_at']


class OrderRefundSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    return_items = OrderReturnDetailSerializer(many=True, read_only=True)
    total_refund_amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderRefund
        fields = [
            'id',
            'order',
            'refund_reason',
            'refund_initiated',
            'refund_completed',
            'notes',
            'admin_approved',
            'approved_at',
            'created_at',
            'updated_at',
            'return_items',
            'total_refund_amount',
        ]

    def get_total_refund_amount(self, obj):
        return obj.total_refund_amount()


class OrderRefundCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRefund
        fields = [
            'order',
            'refund_reason',
            'notes',
        ]


class OrderRefundUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRefund
        fields = [
            'refund_reason',
            'refund_initiated',
            'refund_completed',
            'notes',
            'admin_approved',
            'approved_at',
        ]
        read_only = ['refund_initiated', 'refund_completed', 'approved_at']
