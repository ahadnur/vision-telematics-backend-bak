from django.db import models

from apps.common.enums import OperationChoice
from apps.products.models import ProductSKU
from apps.utilities.models import BaseModel


class Inventory(BaseModel):
	product_sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE, related_name='product_skus')
	stock_quantity = models.IntegerField(default=0)

	def __str__(self):
		return f"Inventory for {self.product_sku.sku_code}"

	class Meta:
		db_table = 'inventory'

	def update_stock(self, quantity, operation_type, reason=None, reference=None):
		"""
		Updates the stock quantity and logs the stock movement.

		:param quantity: Number of items to add or remove.
		:param operation_type: Type of operation ('add', 'remove', 'adjust').
		:param reason: Reason for the stock movement.
		:param reference: Reference ID (e.g., order ID, purchase order ID).
		"""
		if quantity <= 0:
			raise ValueError("Quantity must be positive.")

		if operation_type == OperationChoice.REMOVE.value and quantity > self.stock_quantity:
			raise ValueError("Not enough stock available.")

		previous_quantity = self.stock_quantity

		if operation_type == OperationChoice.ADD.value:
			self.stock_quantity += quantity
		elif operation_type == OperationChoice.REMOVE.value:
			self.stock_quantity -= quantity
		elif operation_type == OperationChoice.ADJUST.value:
			self.stock_quantity = quantity
		else:
			raise ValueError("Invalid operation type.")

		self.save()
		StockMovement.objects.create(
			product_sku=self.product_sku,
			inventory=self,
			operation_type=operation_type,
			quantity=quantity,
			previous_quantity=previous_quantity,
			new_quantity=self.stock_quantity,
			reason=reason,
			reference=reference,
		)


class StockMovement(BaseModel):
	product_sku = models.ForeignKey(
		ProductSKU, on_delete=models.CASCADE, related_name='stock_movements'
	)
	inventory = models.ForeignKey(
		Inventory, on_delete=models.CASCADE, related_name='stock_movements'
	)
	operation_type = models.CharField(max_length=10, choices=OperationChoice)
	quantity = models.PositiveIntegerField()
	previous_quantity = models.PositiveIntegerField()
	new_quantity = models.PositiveIntegerField()
	reason = models.TextField(null=True, blank=True)
	reference = models.CharField(max_length=100, null=True, blank=True)  # E.g., PO or Order ID

	def __str__(self):
		return (
			f"{self.operation_type} {self.quantity} units "
			f"of {self.product_sku.sku_code} (Ref: {self.reference})"
		)

	class Meta:
		db_table = 'stock_movement'
		ordering = ['-created_at']


