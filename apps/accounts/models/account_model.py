from django.db import models

from .company_model import Company
from apps.customers.models import Customer
from apps.utilities.models import BaseModel


class InstallLevel(BaseModel):
    install_level = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'install_level'
        ordering = ['-created_at']

    def __str__(self):
        return self.install_level


class Account(BaseModel):
    account_contact = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, unique=True)
    account_type = models.CharField(max_length=50, choices=[("company", "Company"), ("individual", "Individual")],
                                    default="individual")
    owner_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='accounts')
    owner_customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='accounts')
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    invoice_terms = models.CharField(max_length=50, null=True, blank=True)
    freeze_account = models.BooleanField(default=False)
    hot_account = models.BooleanField(default=False)
    reseller_account = models.BooleanField(default=False)
    confirmation_email = models.EmailField(max_length=100, null=True, blank=True)
    send_confirmation = models.BooleanField(default=False)

    def __str__(self):
        return self.account_number

    class Meta:
        db_table = 'invoice_account'
        ordering = ['-created_at']
