from django.db import models

from apps.utilities.models import BaseModel


class Service(BaseModel):
    service_ref = models.CharField(max_length=100)
    purchase_date = models.DateField()
    first_return_visit = models.DateField(null=True, blank=True)
    fault_reported_date = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=100)  # Stores the contact name associated with the service.
    service_call_date = models.DateField()
    time = models.TimeField()
    nature_of_fault = models.CharField(max_length=255, null=True, blank=True)
    equipment_details = models.TextField()
    notes = models.TextField(null=True, blank=True)
    date_resolved = models.DateField(null=True, blank=True)  # Records the date when the service issue was resolved.
    customer_satisfied = models.BooleanField(default=False)
    invoice_received_date = models.DateField(null=True, blank=True)
    invoice_authorised_date = models.DateField(null=True, blank=True)
    maintenance = models.BooleanField(default=False)
    engineer = models.ForeignKey('engineers.Engineer', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey('customers.Customer', related_name='customer_services',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    install_level = models.ForeignKey('accounts.InstallLevel', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.service_ref


class CustomerCare(models.Model):
    invoice_reference = models.CharField(max_length=100, blank=True, null=True)
    actioned_by = models.ForeignKey('accounts.User', related_name='actions_occured_by', on_delete=models.SET_NULL, null=True, blank=True)  # who initiate or perform action first.
    date = models.DateField(blank=True, null=True)
    action_title = models.CharField(max_length=255, blank=True, null=True)
    detail = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)
    resolved_by = models.ForeignKey('accounts.User', related_name='actions_resolved_by', on_delete=models.SET_NULL, null=True, blank=True)  # who resolve this issue
    service_call = models.CharField(max_length=100, blank=True, null=True)
    service_call_date = models.DateField(blank=True, null=True)
    action_required = models.CharField(max_length=255, blank=True, null=True)
    call_back_reason = models.CharField(max_length=100, blank=True, null=True)
    taken_by = models.ForeignKey('accounts.User', related_name='actions_taken_by', on_delete=models.SET_NULL, null=True, blank=True)  # responsible for handle this issue
    tag = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.invoice_reference
