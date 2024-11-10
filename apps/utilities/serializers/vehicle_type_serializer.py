from rest_framework import serializers
from apps.utilities.models import VehicleType


class VehicleTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = VehicleType
		fields = '__all__'
