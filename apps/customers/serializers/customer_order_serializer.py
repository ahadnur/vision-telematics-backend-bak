from rest_framework import serializers

from apps.customers.models import CustomerVehicle


class CustomerVehicleDropdownForOrderSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.CharField(source='vehicle_make.make_name')

    class Meta:
        model = CustomerVehicle
        fields = ['id', 'vehicle_make']


class CustomerVehicleSerializer(serializers.ModelSerializer):
    vehicle_model = serializers.CharField(source='vehicle_model.model_name')

    class Meta:
        model = CustomerVehicle
        fields = ['id', 'vehicle_model', 'vehicle_type', 'registration_number']