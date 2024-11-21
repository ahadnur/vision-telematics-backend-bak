from rest_framework import serializers
from apps.customers.models import Customer, CustomerVehicleInfo
from apps.utilities.models import VehicleMake, VehicleModel, VehicleType


class CustomerVehicleInfoSerializer(serializers.ModelSerializer):
	customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
	vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.objects.all())
	vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
	vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

	class Meta:
		model = CustomerVehicleInfo
		fields = ['customer', 'vehicle_make', 'vehicle_model', 'vehicle_type', 'registration_number']


class CustomerVehicleSerializer(serializers.ModelSerializer):
	customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
	vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.objects.all())
	vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
	vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

	class Meta:
		model = CustomerVehicleInfo
		fields = ['customer', 'registration_number', 'vehicle_make', 'vehicle_model', 'vehicle_type']
