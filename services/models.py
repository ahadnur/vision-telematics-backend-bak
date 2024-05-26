from django.db import models


class Service(models.Model):
    ref_id = models.CharField(max_length=100)
    service_ref = models.CharField(max_length=100)
    purchase_date = models.DateField()
    first_return_visit = models.DateField(null=True, blank=True)
    fault_reported_date = models.DateField(null=True, blank=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    contact = models.CharField(max_length=100)
    service_call_date = models.DateField()
    time = models.TimeField()
    nature_of_fault = models.TextField()
    equipment_details = models.TextField()
    engineer = models.ForeignKey('Engineer', on_delete=models.SET_NULL)
    notes = models.TextField(null=True, blank=True)
    date_resolved = models.DateField(null=True, blank=True)
    customer_satisfied = models.BooleanField(default=False)
    service_reference = models.CharField(max_length=100, null=True, blank=True)
    invoice_received_date = models.DateField(null=True, blank=True)
    invoice_authorised_date = models.DateField(null=True, blank=True)
    maintenance = models.BooleanField(default=False)


class CustomerCare(models.Model):
    invoice_reference = models.CharField(max_length=100, blank=True, null=True)
    actioned_by = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    action_title = models.CharField(max_length=255, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    resolved_by = models.CharField(max_length=100, blank=True, null=True)
    service_call = models.CharField(max_length=100, blank=True, null=True)
    service_call_date = models.DateField(blank=True, null=True)
    action_required = models.CharField(max_length=255, blank=True, null=True)
    id = models.AutoField(primary_key=True)
    call_back_reason = models.CharField(max_length=100, blank=True, null=True)
    taken_by = models.CharField(max_length=100, blank=True, null=True)
    tag = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.invoice_reference


class WarrantyCallType(models.Model):
    warranty_call_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.warranty_call_type
