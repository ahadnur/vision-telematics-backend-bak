from rest_framework import serializers
from .models import Service
from ..accounts.models import InstallLevel
from ..customers.models import Customer
from ..engineers.models import Engineer
from ..orders.models import Order


class ServiceSerializer(serializers.ModelSerializer):
	engineer = serializers.PrimaryKeyRelatedField(
		queryset=Engineer.objects.filter(is_active=True, is_deleted=False),
		allow_null=True,
	)
	order = serializers.PrimaryKeyRelatedField(
		queryset=Order.objects.filter(is_active=True, is_deleted=False),
		allow_null=True,
	)
	customer = serializers.PrimaryKeyRelatedField(
		queryset=Customer.objects.filter(is_active=True, is_deleted=False),
		allow_null=True,
	)
	install_level = serializers.PrimaryKeyRelatedField(
		queryset=InstallLevel.objects.filter(is_active=True, is_deleted=False),
		allow_null=True,
	)

	class Meta:
		model = Service
		fields = [
			'id',
			'service_ref',
			'purchase_date',
			'first_return_visit',
			'fault_reported_date',
			'contact',
			'service_call_date',
			'time',
			'nature_of_fault',
			'equipment_details',
			'notes',
			'date_resolved',
			'customer_satisfied',
			'invoice_received_date',
			'invoice_authorised_date',
			'maintenance',
			'engineer',
			'order',
			'customer',
			'install_level',
		]
