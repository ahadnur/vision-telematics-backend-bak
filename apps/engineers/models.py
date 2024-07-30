from django.db import models


class EngineerPriority(models.Model):
    engineer_priority = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.engineer_priority


class Engineer(models.Model):
    engineer_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    postcode_coverage = models.CharField(max_length=255, null=True, blank=True)
    # service and pricing
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email_address = models.EmailField(null=True, blank=True)
    out_of_hours = models.BooleanField(default=False)
    address = models.TextField(null=True, blank=True)
    office_number = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    insurance_expires = models.DateField(null=True, blank=True)
    insurance_docs_received = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)
    current_sla = models.CharField(max_length=255, null=True, blank=True)
    performance_rating = models.CharField(max_length=2, choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4)])
    confirm_by = models.CharField(max_length=50, null=True, blank=True)  # mail or fax
    engineer_priority = models.ForeignKey('engineers.EngineerPriority', on_delete=models.SET_NULL, null=True, blank=True)
    job = models.ForeignKey('settings.InstallType', on_delete=models.SET_NULL, null=True, blank=True)
    # company = models.ForeignKey('customers.CustomerCompany', related_name="e_company", related_query_name="company",
    #                             on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.contact_name


class EngineerInvoice(models.Model):
    sp_comms_ref = models.CharField(max_length=255, null=True, blank=True)
    eng_invoice_received = models.DateField(null=True, blank=True)
    eng_invoice_paid = models.DateField(null=True, blank=True)
    invoice_notes = models.TextField(null=True, blank=True)
    engineer = models.ForeignKey(Engineer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.sp_comms_ref

