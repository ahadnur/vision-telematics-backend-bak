from django.db import models


class EngineerPriority(models.Model):
    engineer_priority = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.engineer_priority


class Engineer(models.Model):
    confirm_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    engineer_priority = models.ForeignKey('EngineerPriority', on_delete=models.SET_NULL, null=True, blank=True)
    job = models.ManyToManyField('InstallType')
    engineer_id = models.CharField(max_length=50, unique=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    postcode_coverage = models.CharField(max_length=255, null=True, blank=True)
    # service and pricing
    is_ck = models.BooleanField(default=False)
    is_sn = models.BooleanField(default=False)
    is_ice = models.BooleanField(default=False)
    is_vsib_approved = models.BooleanField(default=False)
    is_alarm_systems = models.BooleanField(default=False)
    is_tracking_systems = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    fax_number = models.CharField(max_length=20, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    install = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    de_install = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    de_and_re = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    # service = models.BooleanField(default=False)
    upgrade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    snav = models.BooleanField(default=False)
    out_of_hours = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)
    office_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    insurance_expires = models.DateField(null=True, blank=True)
    insurance_docs_received = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)
    current_sla = models.CharField(max_length=255, null=True, blank=True)
    performance_rating = models.CharField(max_length=2, choices=[('1', 1),('2', 2),('3', 3), ('4', 4) ])


    def __str__(self):
        return self.contact_name


class EngineerInvoice(models.Model):
    sp_comms_ref = models.CharField(max_length=255, null=True, blank=True)
    eng_invoice_received = models.DateField(null=True, blank=True)
    eng_invoice_paid = models.DateField(null=True, blank=True)
    invoice_notes = models.TextField(null=True, blank=True)
    engineer = models.ForeignKey('Engineer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.sp_comms_ref


class Staff(models.Model):
    staff_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.staff_name
