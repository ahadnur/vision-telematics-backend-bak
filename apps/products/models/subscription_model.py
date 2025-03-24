from datetime import timedelta
from django.db import models
from django.utils.timezone import now

from apps.accounts.models import User, Company
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
    features = models.JSONField() # i do not have enough info from client to add, so i added json field for now

    def __str__(self):
        return f"{self.name} - {self.tier} - {self.price} - {self.billing_cycle}"


class CompanySubscription(BaseModel):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='company_subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='company_subscriptions')
    current_start_date = models.DateField(null=True, blank=True)
    current_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=SubscriptionStatusChoices.choices, 
        default=SubscriptionStatusChoices.ACTIVE
    )
    auto_renew = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.current_end_date:
            if self.plan.billing_cycle == BillingCycleChoices.MONTHLY:
                self.current_end_date = self.current_start_date + timedelta(days=30)
            elif self.plan.billing_cycle == BillingCycleChoices.ANNUAL:
                self.current_end_date = self.current_start_date + timedelta(days=365)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company.company_name} - {self.plan.name} - {self.status}"


class UsageMetrics(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='usage_metrics')
    discount = models.DecimalField(decimal_places=2, max_digits=4, default=0.00)
    discount_count = models.PositiveIntegerField(default=0)
    reset_date = models.DateField()

    def reset_usage(self):  
        self.discount = 0
        self.discount_count = 0
        self.reset_date = now().date() 
        self.save()

    def __str__(self):
        return f"{self.company.company_name} - {self.discount} - {self.discount_count}"


class SubscriptionTransaction(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='subscription_transactions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscription_transactions')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=SubscriptionStatusChoices.choices)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)  # Payment gateway reference

    def save(self, *args, **kwargs):
        if self.start_date and not self.end_date:  # Set end_date when creating subscription
            if self.plan.billing_cycle == BillingCycleChoices.MONTHLY:
                self.end_date = self.start_date + timedelta(days=30)
            elif self.plan.billing_cycle == BillingCycleChoices.ANNUAL:
                self.end_date = self.start_date + timedelta(days=365)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company.company_name} {self.plan.name} {self.status}"
