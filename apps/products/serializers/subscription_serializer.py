from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from apps.products.models import (
    SubscriptionPlan,
    SubscribeAPlan,
    UsageMetrics,
    SubscriptionTransaction
)
from apps.accounts.models import Company, Customer
from apps.common.enums import SubscriptionStatusChoices


class ContentTypeField(serializers.Field):
    """Handles ContentType object <-> model name conversion"""
    def to_representation(self, value):
        return value.model if value else None

    def to_internal_value(self, data):
        try:
            return ContentType.objects.get(model=data.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError("Invalid content type")


class SubscriberField(serializers.Field):
    """Handles generic subscriber relationship"""
    def to_representation(self, value):
        if isinstance(value, Company):
            return {'type': 'company', 'id': value.id, 'name': value.company_name}
        elif isinstance(value, Customer):
            return {'type': 'customer', 'id': value.id, 'ref_number': value.customer_ref_number}
        return None

    def to_internal_value(self, data):
        return {
            'subscriber_type': ContentType.objects.get(model=data['type']),
            'subscriber_id': data['id']
        }


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'tier', 'price', 
            'billing_cycle', 'features'
        ]
        read_only_fields = ['id']

    def validate_features(self, value):
        required = ['discount', 'discount_count']
        if any(key not in value for key in required):
            raise serializers.ValidationError(
                f"Features must include {', '.join(required)}"
            )
        return value


class SubscribeAPlanSerializer(serializers.ModelSerializer):
    subscriber = SubscriberField(source='*', read_only=True)
    subscriber_type = ContentTypeField(write_only=True)
    subscriber_id = serializers.IntegerField(write_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    status = serializers.ChoiceField(
        choices=SubscriptionStatusChoices.choices,
        default=SubscriptionStatusChoices.ACTIVE
    )

    class Meta:
        model = SubscribeAPlan
        fields = [
            'id', 'subscriber', 'subscriber_type', 'subscriber_id',
            'plan', 'plan_name', 'current_start_date', 'current_end_date',
            'status', 'auto_renew'
        ]
        read_only_fields = ['id', 'current_end_date']
        extra_kwargs = {
            'plan': {'write_only': True}
        }

    def validate(self, data):
        if data['subscriber_type'].model not in ['company', 'customer']:
            raise serializers.ValidationError(
                "Subscriber must be a Company or Customer"
            )
        return data


class UsageMetricsSerializer(serializers.ModelSerializer):
    subscriber = SubscriberField(source='*', read_only=True)
    subscriber_type = ContentTypeField(write_only=True)
    subscriber_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UsageMetrics
        fields = [
            'id', 'subscriber', 'subscriber_type', 'subscriber_id',
            'discount', 'discount_count', 'discount_used', 'reset_date'
        ]
        read_only_fields = ['id', 'reset_date']


class SubscriptionTransactionSerializer(serializers.ModelSerializer):
    subscriber = SubscriberField(source='*', read_only=True)
    subscriber_type = ContentTypeField(write_only=True)
    subscriber_id = serializers.IntegerField(write_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)

    class Meta:
        model = SubscriptionTransaction
        fields = [
            'id', 'subscriber', 'subscriber_type', 'subscriber_id',
            'plan', 'plan_name', 'amount_paid', 'start_date', 'end_date',
            'payment_reference', 'note'
        ]
        read_only_fields = ['id', 'amount_paid']
        extra_kwargs = {
            'payment_reference': {'validators': []}
        }

    def validate(self, data):
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError(
                "End date must be after start date"
            )
        return data