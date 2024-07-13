from django.db import models
from apps.utilities.models import TimeStamp


class Order(TimeStamp):
    order_ref_number = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    current_route = models.TextField(blank=True, null=True)
    engineer = models.ForeignKey('Engineer', on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_order')
    customer = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"order created for {self.customer.contact_name}"


class KIF(models.Model):
    """KIF means Kit Instalation Field. Imagine a scenario where a customer buys a toolkit for vehicle installation
    from your store. The KIF table would be used to track details about this purchase and any subsequent returns or
    credits."""

    """KIF means Kit Instalation Field"""

    order = models.ForeignKey('Order', on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    credit_note = models.ForeignKey('Credit', on_delete=models.CASCADE, null=True, blank=True)
    # `returned` means kit back, so credit note should add why returned. otherwise `credit_note` will become null.
    returned = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = "KIFs"


