from rest_framework import serializers

from apps.customers.models import Customer, CustomerVehicle, CustomerAddress
from apps.orders.models import Order, OrderOptionsData
from apps.settings.models import InstallType
from apps.utilities.models import VehicleMake, VehicleModel, VehicleType


class OrderProductSKUSerializer(serializers.Serializer):
    sku_code = serializers.CharField()
    qty = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class PaymentDataSerializer(serializers.Serializer):
    invoice_account_id = serializers.IntegerField()
    invoice_address = serializers.CharField()
    requested_by = serializers.CharField()
    po_number = serializers.CharField()


class OrderCustomerVehicleSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.active_objects.all())
    vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.active_objects.all())
    vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.active_objects.all())

    class Meta:
        model = CustomerVehicle
        fields = ['id', 'vehicle_make', 'vehicle_model', 'vehicle_type', 'registration_number']


class OrderCustomerAddress(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.active_objects.all())

    class Meta:
        model = CustomerAddress
        fields = ['id', 'customer', 'address_line_1', 'address_line_2', 'address_line_3', 'address_line_4', 'postcode']


class OptionDataSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=InstallType.active_objects.all())

    class Meta:
        model = OrderOptionsData
        fields = ['id', 'service', 'existing_kit', 'available_date', 'is_wrapped_job', 'wrapper']


class OrderSerializer(serializers.ModelSerializer):
    payment_data = PaymentDataSerializer(required=False)
    order_product_skus = OrderProductSKUSerializer(many=True, required=False)
    customer_vehicle_info = OrderCustomerVehicleSerializer(source='vehicle', allow_null=False)
    order_options = OptionDataSerializer(required=False)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_status', 'purchasing_notes', 'engineer_notes', 'order_options', 'customer_vehicle_info',
                  'order_product_skus', 'payment_data', 'shipping_charge', 'shipping_address', 'billing_address', 'order_ref_number']