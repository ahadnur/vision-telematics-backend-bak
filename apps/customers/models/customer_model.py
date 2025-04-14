from django.db import models
from apps.utilities.models import BaseModel, VehicleMake, VehicleType, VehicleModel
from apps.common.enums import CustomerFeedbackStatusChouces


class Customer(BaseModel):
    customer_ref_number = models.CharField(max_length=100, unique=True)
    actinic_reference = models.CharField(max_length=100, blank=True, null=True)
    contact_name = models.CharField(max_length=100, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    phone_numbers = models.CharField(max_length=100, blank=True, null=True)
    multi_site_link = models.CharField(max_length=255, blank=True, null=True)
    has_multi_site_link = models.BooleanField(default=False)
    is_web = models.BooleanField(default=False)
    company = models.ForeignKey('accounts.Company', related_name='companies', on_delete=models.SET_NULL,
                                blank=True, null=True)
    payment_reference = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']

    def __str__(self):
        return self.contact_name


class CustomerAddress(BaseModel):
    customer = models.OneToOneField(Customer, related_name='address', on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    address_line_3 = models.CharField(max_length=255, blank=True, null=True)
    address_line_4 = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=20)
    address_type = models.CharField(max_length=50,
                                    choices=[('INSTALL', 'Install'), ('DELIVERY', 'Delivery'), ('INVOICE', 'Invoice')])

    def __str__(self):
        return f"{self.customer.contact_name} - {self.address_type}"


class CustomerVehicle(BaseModel):
    customer = models.ForeignKey(Customer, related_name='vehicles', on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=20)
    vehicle_make = models.ForeignKey(VehicleMake, related_name="make", on_delete=models.SET_NULL, null=True, blank=True)
    vehicle_model = models.ForeignKey(VehicleModel, related_name='model', on_delete=models.SET_NULL, null=True,
                                      blank=True)
    vehicle_type = models.ForeignKey(VehicleType, related_name='type', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.customer.contact_name} - {self.registration_number} - {self.vehicle_make} - {self.vehicle_model}"

    class Meta:
        db_table = 'customer_vehicles'
        ordering = ['-created_at']


class CustomerInstallation(BaseModel):
    customer = models.ForeignKey(Customer, related_name='installations', on_delete=models.CASCADE)
    kit_installed = models.CharField(max_length=100, blank=True, null=True)
    job_required = models.CharField(max_length=255, blank=True, null=True)
    booking_notes = models.TextField(blank=True, null=True)
    date_of_install = models.DateField(blank=True, null=True)
    time_of_install = models.TimeField(blank=True, null=True)
    install_notes = models.TextField(blank=True, null=True)
    preferred_install_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Installation for {self.customer.contact_name} on {self.date_of_install}"


class CustomerNotification(BaseModel):
    customer = models.ForeignKey(Customer, related_name='notifications', on_delete=models.CASCADE)
    customer_notified = models.BooleanField(default=False)
    customer_notified_time = models.DateTimeField(blank=True, null=True)
    email_request_confirmed = models.BooleanField(default=False)
    request_time_stamp = models.DateTimeField(blank=True, null=True)
    courtesy_call = models.BooleanField(default=False)
    courtesy_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Notification for {self.customer.contact_name}"


class CustomerComplaint(BaseModel):
    """
    The CustomerComplaint model represents a complaint made by the customer. This model is used to track issues or
    concerns that a customer has raised regarding the service or products they have received.
    """
    customer = models.ForeignKey(Customer, related_name='complaints', on_delete=models.CASCADE)
    service_call_rod = models.CharField(max_length=100, blank=True, null=True)
    service_call_reference = models.CharField(max_length=100, blank=True, null=True)
    original_complaint_date_time = models.DateTimeField(blank=True, null=True)
    complaint_detail = models.TextField(blank=True, null=True)
    who_took_complaint = models.ForeignKey('accounts.User', related_name='complaints_taken', on_delete=models.SET_NULL,
                                           blank=True, null=True)
    complaint_resolution = models.TextField(blank=True, null=True)
    resolution_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Complaint for {self.customer.contact_name}"


class CustomerKit(BaseModel):
    customer = models.ForeignKey(Customer, related_name='kits', on_delete=models.CASCADE)
    kit_supplied = models.BooleanField(default=False)
    po_number_kit = models.CharField(max_length=100, blank=True, null=True)
    kit_order_date = models.DateField(blank=True, null=True)
    kit_delivered_to = models.CharField(max_length=255, blank=True, null=True)
    kit_delivery_date = models.DateField(blank=True, null=True)
    kit_confirm_delivery = models.DateField(blank=True, null=True)
    delivery_notes = models.CharField(max_length=255, blank=True, null=True)
    courier_tracking_number = models.CharField(max_length=100, blank=True, null=True)
    invoice_received = models.DateTimeField(null=True, blank=True)
    invoice_paid = models.DateTimeField(null=True, blank=True)
    invoice_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Kit and Invoice for {self.customer.contact_name}"


class CustomerMiscellaneous(BaseModel):
    customer = models.ForeignKey(Customer, related_name='miscellaneous', on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    is_purchasing_complete = models.BooleanField(default=False)
    purchasing_complete_time = models.DateTimeField(blank=True, null=True)
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
    existing_kit = models.CharField(max_length=255, null=True, blank=True)
    package = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Miscellaneous for {self.customer.contact_name}"


class Credit(BaseModel):
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


class CustomerFeedback(BaseModel):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='feedbacks')
    product = models.ForeignKey('products.ProductSKU', on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveSmallIntegerField() # 1-10 or 1-5
    feedback = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, 
        choices=CustomerFeedbackStatusChouces.choices, 
        default=CustomerFeedbackStatusChouces.PENDING
    )
    order_referance = models.ForeignKey(
        'orders.Order', 
        on_delete=models.SET_NULL, 
        null=True, blank=True, 
        related_name='feedbacks'
    )

    def __str__(self):
        return f'Feedback by {self.customer} on {self.product} ({self.rating}⭐)'

    class Meta:
        ordering = ['-created_at']
        # unique_together = ('customer', 'product')
        db_table = 'customer_feedback'
        indexes = [
            models.Index(fields=['customer']),
            models.Index(fields=['product']),
            models.Index(fields=['rating']),
            models.Index(fields=['status']),
            models.Index(fields=['order_referance']),
            models.Index(fields=['-created_at']),
        ]
