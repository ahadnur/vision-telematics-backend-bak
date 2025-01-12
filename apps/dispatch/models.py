from django.db import models

from apps.utilities.models import BaseModel


class Dispatch(BaseModel):
    city_link_account = models.CharField(max_length=100, blank=True, null=True)
    invoice_reference = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    add2 = models.CharField(max_length=100, blank=True, null=True)
    add3 = models.CharField(max_length=100, blank=True, null=True)
    add4 = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.CharField(max_length=20, blank=True, null=True)
    service_level = models.CharField(max_length=100, blank=True, null=True)
    delivery_instructions = models.TextField(blank=True, null=True)
    pud = models.BooleanField(default=False)
    returns = models.BooleanField(default=False)
    sat_delivery = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    labels = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'dispatch'
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_reference


class DeliveryRoute(models.Model):
    delivery_route = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.delivery_route

