from django.db import models


class ContactHistoryReason(models.Model):
    contact_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.contact_reason


class ContactHistoryStatus(models.Model):
    contact_history_status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.contact_history_status


class CreditReason(models.Model):
    credit_reason = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.credit_reason


class PaymentMethod(models.Model):
    payment_method = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.payment_method


class POSupplierRef(models.Model):
    po_supplier_ref = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.po_supplier_ref



class InstallType(models.Model):
    install_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.install_type


class CallBackReason(models.Model):
    cat1 = models.CharField(max_length=100, blank=True, null=True)
    cat2 = models.CharField(max_length=100, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.cat1} - {self.cat2}"


class CallBackReasonOld(models.Model):
    reason = models.CharField(max_length=100, blank=True, null=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.reason


class Manager(models.Model):
    staff_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.staff_name
