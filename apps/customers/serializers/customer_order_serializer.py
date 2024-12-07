from rest_framework import serializers

from apps.accounts.models import Account
from apps.customers.models import Customer, CustomerInstallation, CustomerAddress, CustomerVehicleInfo


class CustomerOrderOptionsSerializer(serializers.ModelSerializer):
	customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

	class Meta:
		model = CustomerInstallation
		fields = ['customer', 'job_required', 'preferred_install_date', 'kit_installed']


class CustomerAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerAddress
		fields = ['address_line_1', 'address_line_2', 'address_line_3', 'address_line_4', 'postcode', 'address_type']


class CustomerAccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['id', 'account_name']


class CustomerVehicleInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerVehicleInfo
		fields = ['registration_number', 'vehicle_make', 'vehicle_model', 'vehicle_type']


class CustomerSerializer(serializers.ModelSerializer):
	vehicles = CustomerVehicleInfoSerializer(many=True, read_only=True)
	addresses = CustomerAddressSerializer(many=True, read_only=True, source='customeraddress_set')
	account = CustomerAccountSerializer(read_only=True)

	class Meta:
		model = Customer
		fields = [
			'customer_ref_number', 'contact_name', 'email_address', 'phone_numbers',
			'is_web', 'has_multi_site_link', 'vehicles', 'addresses', 'account'
		]

