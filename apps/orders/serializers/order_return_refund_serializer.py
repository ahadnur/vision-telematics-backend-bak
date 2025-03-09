from rest_framework import serializers

from apps.orders.models import ReturnItem, OrderRefund
from apps.orders.serializers import OrderSerializer


class OrderReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnItem
        fields = [
            'id',
            'order_refund',
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
            'order_refund',
            'order_item',
            'quantity',
            'pickup_address',
            'drop_off_address',
            'reason',
            'shipment_mode',
            'cancellation_charges',
            'notes',
        ]


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


class OrderRefundSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    return_items = OrderReturnSerializer(many=True, read_only=True)
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
