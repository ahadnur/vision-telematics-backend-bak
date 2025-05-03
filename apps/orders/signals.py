from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.orders.models import Order
from apps.orders.tasks import send_order_email

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        subject = "Order Placed Successfully"
        status_message = "placed"
    else:
        subject = "Order Status Updated"
        status_message = f"updated to {instance.order_status}"

    context = {
        "title": subject,
        "customer_name": instance.customer.contact_name or instance.customer.email_address,
        "order_id": instance.order_ref_number,
        "status_message": status_message,
    }

    recipient_email = instance.customer.email_address
    send_order_email.delay(subject, "orders/send_order_mail.html", context, recipient_email)