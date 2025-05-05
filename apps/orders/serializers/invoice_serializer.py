from rest_framework import serializers
from apps.orders.models import CustomerInvoice, EngineerInvoice


class CustomerInvoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInvoice
        fields = [
            'id', 'order', 'invoice_number', 'invoice_date',
            'total_amount', 'payment_status',
        ]


class CustomerInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerInvoice
        fields = [
            'id', 'order', 'invoice_number', 'invoice_date',
            'due_date', 'subtotal', 'total_discount', 
            'tax_rate', 'tax_amount', 'shipping_charge',
            'total_amount', 'billing_address',
            'shipping_address', 'payment_status'
        ]
        read_only_fields = [
            'id', 'invoice_date'
        ]


class EngineerInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineerInvoice
        fields = [
            'id', 'booking', 'invoice_number',
            'invoice_date', 'due_date', 'service_date',
            'total_amount', 'notes'
        ]
        read_only_fields = [
            'id', 'invoice_date'
        ]