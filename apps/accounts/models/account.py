from django.db import models
from apps.utilities.models import TimeStamp


class InstallLevel(models.Model):
    install_levl = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.install_levl


class Account(TimeStamp):
    # account_name and company_name same
    account_name = models.CharField(max_length=255)  # invoice account
    accounts_contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    in_add = models.CharField(max_length=255, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    install_level = models.ForeignKey('InstallLevel', related_name='install_levels',
                                      on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    invoice_terms = models.CharField(max_length=50, null=True, blank=True,)  # maybe days.
    opened = models.DateTimeField(null=True, blank=True)
    opened_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    freeze_account = models.BooleanField(default=False)
    hot_account = models.BooleanField(default=False)
    reseller_account = models.BooleanField(default=False)
    confirmation_email = models.EmailField(max_length=100, null=True, blank=True)
    send_confirmation = models.BooleanField(default=False)

    sales_contact = models.CharField(max_length=100, null=True, blank=True)
    sales_contact_number = models.CharField(max_length=20, null=True, blank=True)
    sales_email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.account_name
