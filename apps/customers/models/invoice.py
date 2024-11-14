from django.db import models

from apps.common.active_manager import ActiveManager
from apps.utilities.models import BaseModel


class Invoice(BaseModel):
    STATUS_CHOICE = [('pending', 'Pending'), ('paid', 'Paid'), ('overdue', 'Overdue')]
    invoice_number = models.CharField(max_length=100)
    customer = models.ManyToManyField('Customer', related_name='customer_invoices')
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, blank=True, null=True)  # e.g., Pending, Paid, Overdue
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['created_at'])
        ]


class InvoiceServiceLog(BaseModel):
    LOG_REQ_TYPE = [('create_invoice', 'Create Invoice'),
                    ('create_customer', 'Create Customer'),
                    ('update_customer', 'Update Customer'),
                    ('other', 'Other'),]

    account_invoice = models.ForeignKey('Invoice', related_name='invoices', on_delete=models.DO_NOTHING, blank=True, null=True)
    status_code = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    request_data = models.TextField(null=True, blank=True)
    response_data = models.TextField(null=True, blank=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)  # DocumentNumber in Fortnox
    retry_count = models.IntegerField(null=False, blank=False, default=0)
    request_type = models.CharField(max_length=100, choices=LOG_REQ_TYPE, default='create_invoice',
                                    null=False, blank=False)
    customer_number = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return str(self.id)