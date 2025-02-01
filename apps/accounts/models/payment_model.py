from django.db import models

from apps.accounts.models import Account
from apps.utilities.models import BaseModel


class Payment(BaseModel):
    invoice_account = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='payment_invoices', null=True)
