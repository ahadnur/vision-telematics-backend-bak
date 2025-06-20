from django.db import models

from apps.utilities.models import BaseModel


class ContactHistoryReason(BaseModel):
    contact_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.contact_reason


class ContactHistoryStatus(BaseModel):
    contact_history_status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.contact_history_status


class CreditReason(BaseModel):
    credit_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.credit_reason


class PaymentMethod(BaseModel):
    payment_method = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.payment_method


class POSupplierRef(BaseModel):
    po_supplier_ref = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.po_supplier_ref


class InstallType(BaseModel):
    install_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'install_type'
        verbose_name_plural = 'Installation Types'
        ordering = ['-created_at']

    def __str__(self):
        return self.install_type


class CallBackReason(BaseModel):
    cat1 = models.CharField(max_length=100, blank=True, null=True)
    cat2 = models.CharField(max_length=100, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.cat1} - {self.cat2}"


class CallBackReasonOld(BaseModel):
    reason = models.CharField(max_length=100, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.reason


class Manager(BaseModel):
    staff_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.staff_name
