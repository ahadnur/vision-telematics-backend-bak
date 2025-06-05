from rest_framework import serializers
from apps.customers.models import Customer, CustomerVehicle
from apps.utilities.models import VehicleMake, VehicleModel, VehicleType


class CustomerVehicleInfoSerializer(serializers.ModelSerializer):
	customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
	vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.objects.all())
	vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
	vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

	class Meta:
		model = CustomerVehicle
		fields = ['customer', 'vehicle_make', 'vehicle_model', 'vehicle_type', 'registration_number']


class CustomerVehicleSerializer(serializers.ModelSerializer):
	customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
	vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.objects.all())
	vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
	vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

	class Meta:
		model = CustomerVehicle
		fields = ['customer', 'registration_number', 'vehicle_make', 'vehicle_model', 'vehicle_type']


class CustomerVehicleListSerializer(serializers.ModelSerializer):
	customer_name = serializers.CharField(read_only=True, required=False)
	make = serializers.CharField(read_only=True, required=False)
	model = serializers.CharField(read_only=True, required=False)
	type = serializers.CharField(read_only=True, required=False)

	class Meta:
		model = CustomerVehicle
		fields = ['id', 'registration_number', 'make', 'model', 'type', 'customer_name']

class VehicleCustomer(serializers.ModelSerializer):
	class Meta:
		model = Customer
		fields = ['id', 'contact_name']

class VehicleMakeSerializer(serializers.ModelSerializer):
	class Meta:
		model = VehicleMake
		fields = ['id', 'make_name']

class VehicleModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = VehicleModel
		fields = ['id', 'model_name']

class VehicleTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = VehicleType
		fields = ['id', 'type_name']


class CustomerSpecificVehicleSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all()
    )
    vehicle_make  = VehicleMakeSerializer(read_only=True)
    vehicle_model = VehicleModelSerializer(read_only=True)
    vehicle_type  = VehicleTypeSerializer(read_only=True)

    class Meta:
        model = CustomerVehicle
        fields = [
            'customer',
            'vehicle_make',
            'vehicle_model',
            'vehicle_type'
        ]