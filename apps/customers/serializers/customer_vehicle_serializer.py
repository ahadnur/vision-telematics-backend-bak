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


class CustomerVehicleListSerializer(serializers.ModelSerializer):
	customer_name = serializers.CharField(read_only=True, required=False)
	make = serializers.CharField(read_only=True, required=False)
	model = serializers.CharField(read_only=True, required=False)
	type = serializers.CharField(read_only=True, required=False)

	class Meta:
		model = CustomerVehicleInfo
		fields = ['id', 'registration_number', 'make', 'model', 'type', 'customer_name']

class VehicleCustomer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ['id', 'contact_name']

class VehicleMakeSerializer(serializers.ModelSerializer):
	class Meta:
		model = VehicleMake
		fields = ['id', 'vehicle_make']

class VehicleModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = VehicleModel
		fields = ['id', 'vehicle_model']

class VehicleTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = VehicleType
		fields = ['id', 'vehicle_type']


class CustomerSpecificVehicleSerializer(serializers.Serializer):
	vehicle_make = serializers.CharField(read_only=True, required=False)
	vehicle_model = serializers.CharField(read_only=True, required=False)
	vehicle_type = serializers.CharField(read_only=True, required=False)
	customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())