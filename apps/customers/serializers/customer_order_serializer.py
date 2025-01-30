from rest_framework import serializers

from apps.customers.models import CustomerVehicle


class CustomerVehicleMakerSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.SerializerMethodField()

    class Meta:
        model = CustomerVehicle
        fields = ['id', 'vehicle_make']

    def get_vehicle_make(self, obj):
        return obj.vehicle_make.make_name


class CustomerVehicleModelSerializer(serializers.ModelSerializer):
    vehicle_model = serializers.SerializerMethodField()

    class Meta:
        model = CustomerVehicle
        fields = ['id', 'vehicle_model', 'vehicle_type', 'registration_number']

    def get_vehicle_model(self, obj):
        return obj.vehicle_model.name