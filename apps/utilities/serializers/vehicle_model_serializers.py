from rest_framework import serializers

from apps.utilities.models import VehicleMake, VehicleModel


class VehicleModelSerializer(serializers.ModelSerializer):
    vehicle_make = serializers.PrimaryKeyRelatedField(
        queryset=VehicleMake.objects.all(),
    )

    class Meta:
        model = VehicleModel
        fields = ['id', 'vehicle_make', 'name']
