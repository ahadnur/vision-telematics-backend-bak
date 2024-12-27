from rest_framework import serializers
from apps.products.models import PO


class POSerializer(serializers.ModelSerializer):
	class Meta:
		model = PO
		fields = [
			'po_ref',
		]
