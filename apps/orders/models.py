from django.db import models

from apps.accounts.models import Account, User
from apps.common.enums import OrderStatusChoice, OrderItemStatusChoice, CustomerPaymentStatusType
from apps.customers.models import CustomerVehicle
from apps.products.models import PO
from apps.settings.models import InstallType
from apps.utilities.models import BaseModel


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
    duration = models.DurationField()
    is_pending = models.BooleanField(default=True)
    booking_status = models.CharField(
        max_length=20,
        choices=[
            ('scheduled', 'Scheduled'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='scheduled'
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

