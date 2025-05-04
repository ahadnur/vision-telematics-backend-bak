from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save
from apps.orders.models import Order
from apps.orders.tasks import send_order_email


@receiver(post_save, sender=Order)
def order_post_save(sender, instance, created, **kwargs):
    if created:
        subject = "Your Order Has Been Placed"
        status_message = "placed successfully"
    else:
        subject = "Your Order Status Has Been Updated"
        status_message = f"updated to {instance.order_status}"


    items = []
    for item in instance.item_orders.filter(is_active=True, is_deleted=False):
        items.append({
            "sku": item.product_sku.sku_code or item.product_sku.product.product_name,
            "name": item.product_sku.product.product_name,
            "quantity": item.quantity,
            "unit_price": item.price,
            "discount": item.discount or 0,
            "total": item.total_price(),
        })

    subtotal = instance.total_price()
    shipping = instance.shipping_charge or 0
    discount = instance.total_discount or 0
    total = subtotal + shipping - discount

    context = {
        "title": subject,
        "customer_name": instance.customer.contact_name or instance.customer.email_address,
        "order_ref": instance.order_ref_number,
        "order_date": instance.created_at,
        "status_message": status_message,
        "items": items,
        "subtotal": subtotal,
        "shipping": shipping,
        "discount": discount,
        "total": total,
        "payment_status": instance.customer_payment_status,
        "shipping_address": instance.shipping_address or {},
        "billing_address": instance.billing_address or {},
        "company_name": "Vision Telematics",
        "support_email": settings.SUPPORT_EMAIL,
        "support_phone": settings.SUPPORT_PHONE,
    }

    recipient = instance.customer.email_address
    send_order_email.delay(subject, "orders/send_order_mail.html", context, recipient)