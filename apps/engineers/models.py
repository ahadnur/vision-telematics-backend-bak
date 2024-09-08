from django.db import models

from apps.utilities.models import TimeStamp


class EngineerCompany(TimeStamp):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'engineer_company'
        verbose_name_plural = 'Engineer Company'
        managed = True

    def __str__(self):
        return self.name


class Engineer(models.Model):
    ENGINEER_PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]
    # details
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    company = models.ForeignKey(EngineerCompany, on_delete=models.SET_NULL, null=True, blank=True)
    engineer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    office_number = models.CharField(max_length=20, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    confirm_method = models.CharField(max_length=50, null=True, blank=True)  # mail or fax
    postcode_coverage = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    # service and pricing

    # out_of_hours = models.BooleanField(default=False)
    # insurance_expires = models.DateField(null=True, blank=True)
    # insurance_docs_received = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)
    current_sla = models.CharField(max_length=255, null=True, blank=True)
    performance_rating = models.CharField(max_length=2, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4)])
    engineer_priority = models.CharField(max_length=10, choices=ENGINEER_PRIORITY_CHOICES, null=True, blank=True)
    job = models.ForeignKey('settings.InstallType', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'engineer'
        verbose_name_plural = 'Engineer'
        managed = True

    def __str__(self):
        return self.contact_name


class EngineerService(TimeStamp):
    engineer = models.OneToOneField(Engineer, on_delete=models.CASCADE, null=True, blank=True)
    is_car_kit_system = models.BooleanField(default=False)
    is_ice_system = models.BooleanField(default=False)
    is_alarm_system = models.BooleanField(default=False)
    is_tracking_system = models.BooleanField(default=False)


class EngineerPricing(TimeStamp):
    engineer = models.OneToOneField(Engineer, on_delete=models.CASCADE, null=True, blank=True)
    installation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    de_re = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    de_installation = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    upgrade = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tracking_install = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class EngineerInvoice(models.Model):
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
