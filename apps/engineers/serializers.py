from django.db import transaction
from rest_framework import serializers

from apps.engineers.models import EngineerCompany, Engineer, EngineerService, EngineerPricing
from apps.settings.serializers import InstallTypeSerializer


class EngieerCompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineerCompany
        fields = ['id', 'name']


class EngineerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineerService
        fields = ['is_car_kit_system', 'is_ice_system', 'is_alarm_system', 'is_tracking_system']


class EngieerPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngineerPricing
        fields = ['installation', 'de_re', 'de_installation', 'upgrade', 'tracking_install']


class EngineerWriteSerializer(serializers.ModelSerializer):
    service = EngineerServiceSerializer(required=False)
    pricing = EngieerPricingSerializer(required=False)

    class Meta:
        model = Engineer
        fields = [
            'contact_name', 'company', 'engineer_id', 'address', 'contact_number', 'office_number',
            'email_address', 'website', 'confirm_method', 'postcode_coverage', 'comments',
            'current_sla', 'performance_rating', 'engineer_priority', 'job', 'service', 'pricing'
        ]

    def create(self, validated_data):
        service_data = validated_data.pop('service')
        pricing_data = validated_data.pop('pricing')
        with transaction.atomic():
            engineer = Engineer.objects.create(**validated_data)
            EngineerService.objects.create(engineer=engineer, **service_data)
            EngineerPricing.objects.create(engineer=engineer, **pricing_data)
        return engineer

    def update(self, instance, validated_data):
        service_data = validated_data.pop('service', None)
        pricing_data = validated_data.pop('pricing', None)

        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            if service_data:
                EngineerService.objects.update_or_create(engineer=instance, defaults=service_data)
            if pricing_data:
                EngineerPricing.objects.update_or_create(engineer=instance, defaults=pricing_data)
            return instance


class EngineerReadSerializer(serializers.ModelSerializer):
    service = EngineerServiceSerializer(read_only=True)
    pricing = EngieerPricingSerializer(read_only=True)
    job = InstallTypeSerializer(read_only=True)

    class Meta:
        model = Engineer
        fields = [
            'id', 'contact_name', 'company', 'engineer_id', 'address', 'contact_number', 'office_number',
            'email_address', 'website', 'confirm_method', 'postcode_coverage', 'comments',
            'current_sla', 'performance_rating', 'engineer_priority', 'job', 'service', 'pricing'
        ]


class GetEngineerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = ['id', 'contact_name']