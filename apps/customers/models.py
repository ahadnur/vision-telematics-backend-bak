from django.db import models
from apps.utilities.models import TimeStamp


class Company(TimeStamp):
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name


class VehicleType(TimeStamp):
    vehicle_type = models.CharField(max_length=100)

    def __str__(self):
        return self.vehicle_type


class VehicleModel(TimeStamp):
    model_name = models.CharField(max_length=100)

    def __str__(self):
        return self.model_name


class Customer(TimeStamp):
    customer_ref_number = models.CharField(max_length=100)
    actinic_reference = models.CharField(max_length=100, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    phone_numbers = models.CharField(max_length=100, blank=True, null=True)
    install_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    delivery_postcode = models.CharField(max_length=20, blank=True, null=True)
    postcode2 = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    registration_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_make = models.CharField(max_length=50, blank=True, null=True)
    vehicle_model = models.CharField(max_length=50, blank=True, null=True)
    kit_installed = models.CharField(max_length=100, blank=True, null=True)  # use product name
    job_required = models.CharField(max_length=255, blank=True, null=True)  # use install type data
    booking_notes = models.TextField(blank=True, null=True)
    requested_by = models.ForeignKey('accounts.User', related_name='made_requests', on_delete=models.SET_NULL, blank=True, null=True)
    date_of_install = models.DateField(blank=True, null=True)
    time_of_install = models.TimeField(blank=True, null=True)
    install_notes = models.TextField(blank=True, null=True)
    customer_notified = models.BooleanField(default=False)
    customer_notified_time = models.DateTimeField(blank=True, null=True)
    email_request_confirmed = models.BooleanField(default=False)
    request_time_stamp = models.DateTimeField(blank=True, null=True)
    courtesy_call = models.BooleanField(default=False)
    courtesy_notes = models.TextField(blank=True, null=True)
    service_call_rod = models.CharField(max_length=100, blank=True, null=True)
    service_call_reference = models.CharField(max_length=100, blank=True, null=True)
    invoice_received = models.DateTimeField(null=True, blank=True)
    invoice_paid = models.DateTimeField(null=True, blank=True)
    invoice_note = models.TextField(blank=True, null=True)
    service_reference = models.CharField(max_length=50, blank=True, null=True)
    original_complaint_date_time = models.DateTimeField(blank=True, null=True)
    complaint_detail = models.TextField(blank=True, null=True)
    who_took_complaint = models.ForeignKey('accounts.User', related_name='made_complaints',
                                           on_delete=models.SET_NULL, blank=True, null=True)
    complaint_resolution = models.TextField(blank=True, null=True)
    resolution_date = models.DateField(blank=True, null=True)
    kit_supplied = models.BooleanField(default=False)  # supplier name
    po_number_kit = models.CharField(max_length=100, blank=True, null=True)  # purchase order(PO) number
    kit_order_date = models.DateField(blank=True, null=True)
    kit_delivered_to = models.CharField(max_length=255, blank=True, null=True)
    kit_delivery_date = models.DateField(blank=True, null=True)
    kit_confirm_delivery = models.DateField(blank=True, null=True)
    delivery_notes = models.CharField(max_length=255, blank=True, null=True)
    courier_tracking_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_address = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    preferred_install_date = models.DateField(blank=True, null=True)
    multi_site_link = models.CharField(max_length=255, blank=True, null=True)
    has_multi_site_link = models.BooleanField(default=False)
    is_purchasing_complete = models.BooleanField(default=False)
    purchasing_complete_time = models.DateTimeField(blank=True, null=True)
    # sales person
    sold_by = models.ForeignKey('accounts.User', related_name='sales', on_delete=models.SET_NULL, blank=True, null=True)
    customer_confirmed_by = models.ForeignKey('accounts.User', related_name='confirmed_customers',
                                              on_delete=models.SET_NULL, blank=True, null=True)
    customer_confirmed_time = models.DateTimeField(blank=True, null=True)
    acc_inv_raised_date = models.DateField(blank=True, null=True)
    acc_inv_paid = models.CharField(max_length=255, blank=True, null=True)
    is_on_hold = models.BooleanField(default=False)
    record_edited_at = models.DateTimeField(blank=True, null=True)
    service_reference_org = models.CharField(max_length=100, blank=True, null=True)
    call_back_reason = models.CharField(max_length=100, blank=True, null=True)
    stock_to_be_returned = models.CharField(max_length=100, blank=True, null=True)
    service_call_enabled = models.BooleanField(default=False)
    call_back_date = models.DateField(blank=True, null=True)
    post_code1 = models.CharField(max_length=20, blank=True, null=True)
    install_address_2 = models.CharField(max_length=255, blank=True, null=True)
    install_address_3 = models.CharField(max_length=255, blank=True, null=True)
    install_address_4 = models.CharField(max_length=255, blank=True, null=True)
    delivery_address_2 = models.CharField(max_length=255, blank=True, null=True)
    delivery_address_3 = models.CharField(max_length=255, blank=True, null=True)
    delivery_address_4 = models.CharField(max_length=255, blank=True, null=True)
    is_web = models.BooleanField(default=False)
    instlev = models.CharField(max_length=100, blank=True, null=True)
    is_dispatch_printed = models.BooleanField(default=False)
    eng_inv_no = models.CharField(max_length=100, blank=True, null=True)
    is_hot = models.BooleanField(default=False)
    jcd = models.DateField(blank=True, null=True)
    sat = models.BooleanField(default=False)
    late = models.IntegerField(blank=True, null=True)
    consignment = models.CharField(max_length=100, blank=True, null=True)
    is_dispute_eng_inv = models.BooleanField(default=False)
    dispute_eng_reason = models.CharField(max_length=100, blank=True, null=True)
    dispute_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, blank=True, null=True)
    back_order = models.BooleanField(default=False)
    existing_kit = models.BooleanField(default=False)
    package = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey('Company', related_name='companies',
                                on_delete=models.SET_NULL, blank=True, null=True)
    account = models.ForeignKey('accounts.Account', related_name='customer_accounts',
                                on_delete=models.SET_NULL, blank=True, null=True)
    engineer = models.ForeignKey('engineers.Engineer', related_name='engineers',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_type = models.ForeignKey('VehicleType', related_name='vehicle_types', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Customers"


class Invoice(TimeStamp):
    STATUS_CHOICE = [('pending', 'Pending'), ('paid', 'Paid'), ('overdue', 'Overdue')]
    invoice_number = models.CharField(max_length=100)
    customer = models.ManyToManyField('Customer', related_name='customer_invoices')
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, blank=True, null=True)  # e.g., Pending, Paid, Overdue
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['created_at']),
            models.Index(fields=['customer']),
        ]


class Credit(TimeStamp):
    name = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    original_invoice = models.ForeignKey('Invoice', on_delete=models.CASCADE, null=True, blank=True)
    credit_note_number = models.CharField(max_length=100, blank=True, null=True)
    account = models.ForeignKey('accounts.Account', on_delete=models.SET_NULL, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    invoice_address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    stock_supplied_to = models.CharField(max_length=100, blank=True, null=True)
    stock_returned = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    authorised = models.BooleanField(default=False)

    def __str__(self):
        return self.credit_note_number


class InvoiceServiceLog(TimeStamp):
    LOG_REQ_TYPE = [('create_invoice', 'Create Invoice'),
                    ('create_customer', 'Create Customer'),
                    ('update_customer', 'Update Customer'),
                    ('other', 'Other'),]

    account_invoice = models.ForeignKey('Invoice', related_name='invoices', on_delete=models.DO_NOTHING, blank=True, null=True)
    status_code = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    request_data = models.TextField(null=True, blank=True)
    response_data = models.TextField(null=True, blank=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)  # DocumentNumber in Fortnox
    retry_count = models.IntegerField(null=False, blank=False, default=0)
    request_type = models.CharField(max_length=100, choices=LOG_REQ_TYPE, default='create_invoice',
                                    null=False, blank=False)
    customer_number = models.CharField(max_length=60, null=True, blank=True)

    def __str__(self):
        return str(self.id)

