from django.db import models

from apps.products.models import PO
from apps.utilities.models import BaseModel


class Order(BaseModel):
    order_ref_number = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    current_route = models.TextField(blank=True, null=True)
    purchasing_notes = models.TextField(blank=True, null=True)
    engineer_notes = models.TextField(blank=True, null=True)
    engineer = models.ForeignKey('engineers.Engineer', related_name='order_engineers', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    customer = models.ForeignKey('customers.Customer', related_name='order_customers', on_delete=models.SET_NULL,
                                 null=True, blank=True)

    def __str__(self):
        return f"Order created for {self.customer.contact_name}"

    def total_price(self):
        return sum(item.total_price() for item in self.item_orders.filter(is_active=True, is_deleted=False))

    def total_quantity(self):
        return sum(item.quantity for item in self.item_orders.filter(is_active=True, is_deleted=False))


# KIF
class OrderItem(BaseModel):
    order = models.ForeignKey('orders.Order', related_name='item_orders', on_delete=models.CASCADE, null=True, blank=True)
    product_sku = models.ForeignKey('products.ProductSKU', related_name='order_item_skus', on_delete=models.CASCADE, blank=True, null=True)
    po = models.ForeignKey(PO, related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)  # Added field
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    credit_note = models.ForeignKey('customers.Credit', related_name='order_item_credits', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.product_sku.sku_code if self.product_sku.sku_code else ''} for Order {self.order.order_ref_number}"

    def total_price(self):
        total = self.price * self.quantity
        if self.discount:
            total -= self.discount
        return total

    def save(self, *args, **kwargs):
        if self.quantity > self.product_sku.qty:
            raise ValueError("Ordered quantity exceeds available stock.")
        super().save(*args, **kwargs)


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

    def __str__(self):
        return f"Booking for {self.order.customer.contact_name} on {self.booking_date} at {self.booking_time}"

