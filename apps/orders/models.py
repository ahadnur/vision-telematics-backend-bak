from django.db import models
from django.core.exceptions import ValidationError

from apps.accounts.models import Account, User
from apps.customers.models import CustomerVehicle
from apps.products.models import PO
from apps.settings.models import InstallType
from apps.utilities.models import BaseModel
from apps.common.enums import (
    OrderStatusChoice, 
    OrderItemStatusChoice, 
    CustomerPaymentStatusType, 
    ReturnStatusType,
    ShipmentMode,
    BookingStatusType,
)


class Order(BaseModel):
    order_status = models.CharField(max_length=20, choices=OrderStatusChoice.choices, default='created')
    order_ref_number = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    shipping_address = models.JSONField(default=dict, null=True, blank=True)
    billing_address = models.JSONField(default=dict, null=True, blank=True)
    purchasing_notes = models.TextField(blank=True, null=True)
    engineer_notes = models.TextField(blank=True, null=True)
    engineer = models.ForeignKey('engineers.Engineer', related_name='order_engineers', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    customer = models.ForeignKey('customers.Customer', related_name='order_customers', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    order_cancellation_reason = models.TextField(blank=True, null=True)
    cancelled_by = models.CharField(max_length=20, null=True, blank=True)
    shipping_charge = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    coupon_id = models.CharField(max_length=20, null=True, blank=True)
    total_discount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    customer_payment_status = models.CharField(max_length=10, null=True, blank=True,
                                               choices=CustomerPaymentStatusType.choices)
    vehicle = models.ForeignKey(CustomerVehicle, related_name='orders', on_delete=models.SET_NULL, null=True,
                                blank=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_ref_number} for {self.customer.contact_name}"

    def total_price(self):
        return sum(item.total_price() for item in self.item_orders.filter(is_active=True, is_deleted=False))

    def total_quantity(self):
        return sum(item.quantity for item in self.item_orders.filter(is_active=True, is_deleted=False))

    def set_status(self, new_status):
        """Update the order status."""
        if new_status not in dict(OrderStatusChoice.choices).keys():
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        self.save()

    def total_price(self):
        return sum(item.total_price() for item in self.item_orders.filter(is_active=True, is_deleted=False))

    def total_quantity(self):
        return sum(item.quantity for item in self.item_orders.filter(is_active=True, is_deleted=False))


class OrderItem(BaseModel):
    order = models.ForeignKey('orders.Order', related_name='item_orders', on_delete=models.CASCADE)
    product_sku = models.ForeignKey('products.ProductSKU', related_name='order_item_skus', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=OrderItemStatusChoice.choices, default='pending')
    returned = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_items'
        ordering = ['-created_at']

    def __str__(self):
        return (f"{self.quantity} x {self.product_sku.sku_code if self.product_sku.sku_code else ''}"
                f" for Order {self.order.order_ref_number}")

    def total_price(self):
        total = self.price * self.quantity
        if self.discount:
            total -= self.discount
        return total

    def save(self, *args, **kwargs):
        if self.quantity > self.product_sku.qty:
            raise ValueError("Ordered quantity exceeds available stock.")
        super().save(*args, **kwargs)

    def set_status(self, new_status):
        """Update the item status."""
        if new_status not in dict(OrderItemStatusChoice.choices).keys():
            raise ValueError(f"Invalid status: {new_status}")
        self.status = new_status
        self.save()

class Booking(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    engineer = models.ForeignKey('engineers.Engineer', on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    duration = models.DurationField()  #==> example: P0DT2H30M0S (for 2hr 30 mins)
    is_pending = models.BooleanField(default=True)
    booking_status = models.CharField(
        max_length=20,
        choices=BookingStatusType.choices,
        default=BookingStatusType.SCHEDULED,
    )
    remarks = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('engineer', 'booking_date', 'booking_time')
        db_table = 'bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking for {self.order.customer.contact_name} on {self.booking_date} at {self.booking_time}"


class OrderOptionsData(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='options_data')
    existing_kit = models.BooleanField(default=False)
    available_date = models.DateField(null=True, blank=True)
    service = models.ForeignKey(InstallType, related_name='options_data', on_delete=models.SET_NULL, null=True,
                                blank=True)
    is_wrapped_job = models.BooleanField(default=False)
    wrapper = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'order_options_data'
        ordering = ['-created_at']


class OrderPaymentOptions(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    invoice_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='invoice_account')
    invoice_address = models.CharField(max_length=255, null=True, blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, )
    po_number = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'order_payment_options'
        ordering = ['-created_at']


class OrderRefund(BaseModel):
    order = models.ForeignKey(Order, related_name='refunds', on_delete=models.CASCADE)
    # payment = models.OneToOneField(Payment, related_name='refund', on_delete=models.RESTRICT, null=True, blank=True)
    refund_reason = models.TextField(null=True, blank=True)
    refund_initiated = models.DateTimeField(null=True, blank=True)
    refund_completed = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    admin_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'order_refunds'
        ordering = ('-created_at',)
        verbose_name = 'Order Refund'
        verbose_name_plural = 'Order Refunds'

    def __str__(self):
        return f'Refund {self.id} of Order {self.order.order_ref_number}'

    def total_refund_amount(self):
        return sum(item.refund_amount for item in self.return_items.all())  # Calculated dynamically


class ReturnItem(BaseModel):
    order_refund = models.ForeignKey(
        OrderRefund, 
        related_name='return_items', 
        on_delete=models.RESTRICT,
        null=True, blank=True
    )
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    return_status = models.CharField(
        max_length=20, 
        choices=ReturnStatusType.choices, 
        default=ReturnStatusType.REQUESTED
    )
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) # auto calculate on save
    pickup_address = models.JSONField(default=dict, null=True, blank=True)
    drop_off_address = models.JSONField(default=dict, null=True, blank=True)
    # user_id = models.UUIDField(db_index=True)
    reason = models.TextField(null=True, blank=True)
    shipment_mode = models.CharField(max_length=32, choices=ShipmentMode.choices, default=ShipmentMode.DROPOFF)
    cancellation_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    return_rejected_reason = models.TextField(null=True, blank=True)
    return_rejected_by = models.CharField(max_length=50, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    is_restocked = models.BooleanField(default=False)
    restocked_at = models.DateTimeField(null=True, blank=True)


    class Meta:
        db_table = 'return_items'

    def __str__(self):
        return f'Return Item {self.id} of Order {self.order_item.order.order_ref_number}'

    def save(self, *args, **kwargs):
        if self.quantity > self.order_item.quantity:
            raise ValidationError("Return quantity exceeds original order quantity")

        if self.order_item.order.customer_payment_status == CustomerPaymentStatusType.PAID:
            self.refund_amount = (
                self.order_item.price * self.quantity - (self.order_item.discount or 0)
            )
        super().save(*args, **kwargs)


class CustomerInvoice(BaseModel):
    order = models.OneToOneField(Order, related_name='customer_invoice', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)  # New field
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0.0, help_text="Amount before discounts/taxes") # new field
    total_discount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Tax rate in percentage (e.g., 18.5%)") # new field
    tax_amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.0) # new field
    shipping_charge = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    billing_address = models.JSONField(default=dict, null=True, blank=True)
    shipping_address = models.JSONField(default=dict, null=True, blank=True) # new field
    payment_status = models.CharField(max_length=10, choices=CustomerPaymentStatusType.choices)

    class Meta:
        db_table = 'customer_invoices'
        ordering = ['-invoice_date']

    def __str__(self):
        return f"Invoice {self.invoice_number} amount({self.total_amount})"

    def save(self, *args, **kwargs):
        """Auto-calculate total_amount if not provided"""
        if not self.total_amount:
            self.total_amount = (
                self.subtotal - self.total_discount + self.tax_amount + self.shipping_charge
            )
        super().save(*args, **kwargs)


class EngineerInvoice(BaseModel):
    order = models.OneToOneField(Order, related_name='engineer_invoice', on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)  # New field
    service_date = models.DateField(null=True, blank=True) # new field
    total_amount = models.DecimalField(max_digits=20, decimal_places=2)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'engineer_invoices'
        ordering = ['-invoice_date']

    def __str__(self):
        return f"Engineer Invoice {self.invoice_number} amount({self.total_amount})"