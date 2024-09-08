from rest_framework import serializers
from .models import InstallType


class InstallTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallType
        fields = ['id', 'install_type']
