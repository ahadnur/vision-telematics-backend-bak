from rest_framework import serializers

from apps.products.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
	class Meta:
		model = Supplier
		fields = ['id', 'supplier_name']

