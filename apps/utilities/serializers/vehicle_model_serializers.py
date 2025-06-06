from rest_framework import serializers

from apps.utilities.models import VehicleMake, VehicleModel


class VehicleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = ['id', 'vehicle_make', 'model_name']
