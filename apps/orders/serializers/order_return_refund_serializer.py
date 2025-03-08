from rest_framework import serializers

from apps.orders.models import ReturnItem, OrderRefund


class OrderReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnItem
        fields = [
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