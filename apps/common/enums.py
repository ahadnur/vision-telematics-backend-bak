from django.db import models


class OperationChoice(models.TextChoices):
    REMOVE = 'remove', 'Remove'
    ADD = 'add', 'Add'
    ADJUST = 'adjust', 'Adjust'


class OrderStatusChoice(models.TextChoices):
    CREATED = 'created', 'Created'
    PROCESSING = 'processing', 'Processing'
    DELIVERED = 'delivered', 'Delivered'
    REJECTED = 'rejected', 'Rejected'
    DRAFT = 'draft', 'Draft'

class OrderItemStatusChoice(models.TextChoices):
    PENDING = 'pending', 'Pending'
    SHIPPED = 'shipped', 'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    REJECTED = 'rejected', 'Rejected'


class CustomerPaymentStatusType(models.TextChoices):
    UNPAID = 'unpaid', 'Unpaid'
    PARTIAL = 'partial', 'Partial'
    PAID = 'paid', 'Paid'


class ReturnStatusType(models.TextChoices):
    REQUESTED = 'requested', 'Requested',
    APPROVED = 'approved', 'Approved',
    REJECTED = 'rejected', 'Rejected',
    COMPLETED = 'completed', 'Completed'


class ShipmentMode(models.TextChoices):
    PICKUP = 'pickup', 'Customer Pickup',
    DROPOFF = 'dropoff', 'Dropoff at Center',
    COURIER = 'courier', 'Courier Service'