from rest_framework import serializers
from apps.customers.models import Customer, CustomerInstallation


class CustomerOrderOptionsSerializer(serializers.ModelSerializer):
	customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

	class Meta:
		model = CustomerInstallation
		fields = ['customer', 'job_required', 'preferred_install_date', 'kit_installed']