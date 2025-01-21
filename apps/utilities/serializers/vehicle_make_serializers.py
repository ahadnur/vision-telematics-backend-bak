from rest_framework import serializers
from apps.utilities.models import VehicleMake


class VehicleMakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleMake
        fields = ['id', 'make_name']
