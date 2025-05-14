from django.db import IntegrityError
from rest_framework import serializers

from apps.accounts.models import Company
from apps.customers.views import logger
from apps.engineers.models import Engineer
from apps.settings.models import InstallType
from apps.settings.serializers import InstallTypeSerializer


class EngineerWriteSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.filter(is_active=True))
    job = serializers.PrimaryKeyRelatedField(queryset=InstallType.objects.filter(is_active=True))

    class Meta:
        model = Engineer
        fields = [
            'contact_name', 'company', 'engineer_id', 'address', 'contact_number', 'office_number',
            'email_address', 'website', 'postcode_coverage', 'comments', 'insurance_expiration',
            'current_sla', 'performance_rating', 'engineer_priority', 'job',
            'is_telematics', 'is_dash_cam', 'is_dvs', 'is_dvr', 'is_adr_tanker',
            'is_specialist_vehicles', 'is_insurance_on_file', 'is_current_sla', 'is_other'
        ]

    def create(self, validated_data):
        try:
            engineer = Engineer.objects.create(**validated_data)
            return engineer
        except IntegrityError as e:
            logger.error(f'update enginer error on: {e}')
            raise serializers.ValidationError(f'{e}')
        except Exception as e:
            logger.error(f'update enginer error on: {e}')
            raise serializers.ValidationError(f'{e}')

    def update(self, instance, validated_data):
        try:
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except IntegrityError as e:
            logger.error(f'update enginer error on: {e}')
            raise serializers.ValidationError(f'{e}')
        except Exception as e:
            logger.error(f'update enginer error on: {e}')
            raise serializers.ValidationError(f'{e}')


class EngineerReadSerializer(serializers.ModelSerializer):
    job = InstallTypeSerializer(read_only=True)

    class Meta:
        model = Engineer
        fields = [
            'id', 'contact_name', 'company', 'engineer_id', 'address', 'contact_number', 'office_number',
            'email_address', 'website', 'postcode_coverage', 'comments', 'insurance_expiration',
            'current_sla', 'performance_rating', 'engineer_priority', 'job',
            'is_telematics', 'is_dash_cam', 'is_dvs', 'is_dvr', 'is_adr_tanker',
            'is_specialist_vehicles', 'is_insurance_on_file', 'is_current_sla', 'is_other'
        ]


class GetEngineerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = ['id', 'contact_name', 'email_address', 'address', 'contact_number']
