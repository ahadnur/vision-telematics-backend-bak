from rest_framework import serializers
from apps.customers.models import Customer, CustomerAddress, CustomerVehicleInfo, CustomerInstallation
from apps.utilities.models import Company, VehicleMake, VehicleModel, VehicleType


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name']


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ('address_line_1', 'address_line_2', 'address_line_3', 'address_line_4', 'postcode')


class CustomerWriteSerializer(serializers.ModelSerializer):
    address = CustomerAddressSerializer()
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())  # Or use `read_only=True` if needed

    class Meta:
        model = Customer
        fields = ['id', 'customer_ref_number', 'contact_name', 'phone_numbers', 'address', 'email_address', 'company']


class CustomerVehicleSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.objects.all())
    vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
    vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

    class Meta:
        model = CustomerVehicleInfo
        fields = ['customer', 'registration_number', 'vehicle_make', 'vehicle_model', 'vehicle_type']


# for oder
class CustomerOrderOptionsSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = CustomerInstallation
        fields = ['customer', 'job_required', 'preferred_install_date', 'kit_installed']


class CustomerVehicleInfoSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.objects.all())
    vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
    vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

    class Meta:
        model = CustomerVehicleInfo
        fields = ['customer', 'vehicle_make', 'vehicle_model', 'vehicle_type', 'registration_number']
