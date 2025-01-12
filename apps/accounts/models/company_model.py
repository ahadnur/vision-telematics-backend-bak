from django.db import models

from apps.utilities.models import BaseModel


class Company(BaseModel):
    company_name = models.CharField(max_length=255, unique=True)
    registration_number = models.CharField(max_length=100, null=True, blank=True)
    primary_contact_name = models.CharField(max_length=255, null=True, blank=True,)
    primary_contact_email = models.EmailField(max_length=255, null=True, blank=True)
    primary_contact_phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'company'
        ordering = ('-created_at',)
