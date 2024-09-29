from django.db import models

from apps.utilities.models import BaseModel


class EngineerCompany(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'engineer_company'
        verbose_name_plural = 'Engineer Company'
        managed = True

    def __str__(self):
        return self.name


class Engineer(BaseModel):
    ENGINEER_PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    contact_name = models.CharField(max_length=255, unique=True, null=True, blank=True)
    company = models.ForeignKey(EngineerCompany, on_delete=models.SET_NULL, null=True, blank=True)
    email_address = models.EmailField(unique=True, null=True, blank=True)
    engineer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    office_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    postcode_coverage = models.CharField(max_length=255, null=True, blank=True)
    insurance_expiration = models.DateField(null=True, blank=True)

    comments = models.TextField(null=True, blank=True)
    current_sla = models.CharField(max_length=255, null=True, blank=True)
    performance_rating = models.CharField(max_length=2, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4)])
    engineer_priority = models.CharField(max_length=10, choices=ENGINEER_PRIORITY_CHOICES, null=True, blank=True)
    job = models.ForeignKey('settings.InstallType', on_delete=models.SET_NULL, null=True, blank=True)

    is_telematics = models.BooleanField(default=False)
    is_dashcam = models.BooleanField(default=False)
    is_dvs = models.BooleanField(default=False)
    is_dvr = models.BooleanField(default=False)
    is_adr_tanker = models.BooleanField(default=False)
    is_specialist_vehicles = models.BooleanField(default=False)
    is_insurance_on_file = models.BooleanField(default=False)
    is_current_sla = models.BooleanField(default=False)
    is_other = models.BooleanField(default=False)

    class Meta:
        db_table = 'engineer'
        verbose_name_plural = 'Engineer'
        managed = True

    def __str__(self):
        return self.contact_name


class EngineerInvoice(BaseModel):
    sp_comms_ref = models.CharField(max_length=255, null=True, blank=True)
    eng_invoice_received = models.DateField(null=True, blank=True)
    eng_invoice_paid = models.DateField(null=True, blank=True)
    invoice_notes = models.TextField(null=True, blank=True)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'engineer_invoice'
        verbose_name_plural = 'Engineer Invoice'
        managed = True

    def __str__(self):
        return self.sp_comms_ref
