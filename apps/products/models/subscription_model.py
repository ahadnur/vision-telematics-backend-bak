from datetime import date
from datetime import timedelta
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.accounts.models import User, Company, Customer
from apps.utilities.models import BaseModel
from apps.common.enums import SubscriptionTierChoices, BillingCycleChoices, SubscriptionStatusChoices


class SubscriptionPlan(BaseModel):
    name = models.CharField(max_length=100)
    tier = models.CharField(
        max_length=20, 
        choices=SubscriptionTierChoices.choices,
        default=SubscriptionTierChoices.BASIC
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(
        max_length=20, 
        choices=BillingCycleChoices.choices,
        default=BillingCycleChoices.MONTHLY
    )
    features = models.JSONField()

    class Meta:
        db_table = 'subscription_plans'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tier']),
            models.Index(fields=['billing_cycle']),
        ]

    def __str__(self):
        return f"{self.name} - {self.tier} - {self.price} - {self.billing_cycle}"

    def clean(self):
        required_features = ['discount', 'discount_count']
        for feature in required_features:
            if feature not in self.features:
                raise ValidationError(f"Missing required feature: {feature}")


class SubscribeAPlan(BaseModel):
    subscriber_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE,
        limit_choices_to={'model__in': ['company', 'customer']}
    )
    subscriber_id = models.PositiveIntegerField()
    subscriber = GenericForeignKey('subscriber_type', 'subscriber_id')

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    current_start_date = models.DateField(default=now)
    current_end_date = models.DateField()
    status = models.CharField(
        max_length=20, 
        choices=SubscriptionStatusChoices.choices, 
        default=SubscriptionStatusChoices.ACTIVE
    )
    auto_renew = models.BooleanField(default=True)

    class Meta:
        db_table = 'subscribed_plans'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber_type', 'subscriber_id'],
                condition=models.Q(status=SubscriptionStatusChoices.ACTIVE),
                name='unique_active_subscription'
            )
        ]
        indexes = [
            models.Index(fields=['subscriber_type', 'subscriber_id']),
            models.Index(fields=['status', 'current_end_date']),
        ]

    def __str__(self):
        return f"{self.subscriber} - {self.plan.name} - {self.status}"

    def clean(self):
        if not self.subscriber_type.model_class() in (Company, Customer):
            raise ValidationError("Invalid subscriber type")
        
        if self.current_end_date <= self.current_start_date:
            raise ValidationError("End date must be after start date")

    def save(self, *args, **kwargs):
        if not self.current_end_date:
            self.current_end_date = self._calculate_end_date()
        super().save(*args, **kwargs)

    def _calculate_end_date(self):
        if self.plan.billing_cycle == BillingCycleChoices.MONTHLY:
            return self.current_start_date + timedelta(days=30)
        elif self.plan.billing_cycle == BillingCycleChoices.ANNUAL:
            return self.current_start_date + timedelta(days=365)
        return self.current_start_date


class UsageMetrics(models.Model):
    subscriber_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    subscriber_id = models.PositiveIntegerField()
    subscriber = GenericForeignKey('subscriber_type', 'subscriber_id')

    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    discount_count = models.PositiveIntegerField(default=0)
    discount_used = models.PositiveIntegerField(default=0)
    reset_date = models.DateField()

    class Meta:
        db_table = 'usage_metrics'
        ordering = ['-reset_date']
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber_type', 'subscriber_id'],
                name='unique_subscriber_metrics'
            )
        ]
        indexes = [
            models.Index(fields=['subscriber_type', 'subscriber_id']),
            models.Index(fields=['reset_date']),
        ]

    def __str__(self):
        return f"{self.subscriber} - Remaining: {self.discount_count}"

    def reset(self):
        self.discount_count = self.discount_used = 0
        self.reset_date = now().date()
        self.save()

    def clean(self):
        if not isinstance(self.subscriber, (Company, Customer)):
            raise ValidationError("Subscriber must be a Company or Customer")


class SubscriptionTransaction(BaseModel):
    subscriber_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    subscriber_id = models.PositiveIntegerField()
    subscriber = GenericForeignKey('subscriber_type', 'subscriber_id')

    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='transactions')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        db_table = 'subscription_transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['subscriber_type', 'subscriber_id']),
            models.Index(fields=['payment_reference']),
        ]

    def __str__(self):
        return f"{self.subscriber} - {self.plan.name} - {self.amount_paid}"

    def clean(self):
        if not isinstance(self.subscriber, (Company, Customer)):
            raise ValidationError("Subscriber must be a Company or Customer")
        
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            self._update_usage_metrics()

    def _update_usage_metrics(self):
        metrics, created = UsageMetrics.objects.get_or_create(
            subscriber_type=self.subscriber_type,
            subscriber_id=self.subscriber_id,
            defaults={
                'discount': self.plan.features['discount'],
                'discount_count': self.plan.features['discount_count'],
                'reset_date': self.end_date
            }
        )
        
        if not created:
            metrics.discount = self.plan.features['discount']
            metrics.discount_count = self.plan.features['discount_count']
            metrics.reset_date = self.end_date
            metrics.save()