from rest_framework import serializers
from apps.products.models import (
    SubscriptionPlan,
    CompanySubscription,
    UsageMetrics,
    SubscriptionTransaction
)


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            'id', 'name', 'tier',
            'price', 'billing_cycle', 
            'features'
        ]
        read_only_fields = ['id']
    

class CompanySubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanySubscription
        fields = [
            'id', 'company', 'plan', 'status'
            'current_start_date', 'current_end_date',
            'auto_renew'
        ]
        read_only_fields = ['id', 'current_end_date']


class UsageMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageMetrics
        fields = [
            'id', 'company', 'discount', 'discount_count', 'reset_date',
        ]
        read_only_fields = ['id']


class SubscriptionTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionTransaction
        fields = [
            'id', 'company', 'plan', 'amount_paid',
            'start_date', 'end_date', 'status',
            'payment_reference', 
        ]
        read_only_fields = ['id', ]