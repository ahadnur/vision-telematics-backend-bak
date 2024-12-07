from django.db import models

from apps.common.enums import OperationChoice
from apps.utilities.models import BaseModel


class Category(BaseModel):
	category_name = models.CharField(max_length=255, null=True, blank=True)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.category_name


class Product(BaseModel):
	product_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
	description = models.TextField(null=True, blank=True)  # Changed to TextField
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
	note = models.TextField(null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)

	def __str__(self):
		return f'{self.product_name}'


# PastError
class ProductSKU(BaseModel):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_skus', null=True, blank=True)
	sku_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
	description = models.TextField(blank=True, null=True)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	qty = models.IntegerField(blank=True, null=True)
	discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	class Meta:
		verbose_name_plural = 'ProductSKUs'

	def __str__(self):
		return str(self.id)

	def save(self, *args, **kwargs):
		if self.unit_price is not None and self.qty is not None:
			self.total = self.unit_price * self.qty
		else:
			self.total = None
		super(ProductSKU, self).save(*args, **kwargs)


class Inventory(BaseModel):
	product_sku = models.ForeignKey(
		'ProductSKU', on_delete=models.CASCADE, related_name='inventory'
	)
	stock_quantity = models.IntegerField(default=0)

	def __str__(self):
		return f"Inventory for {self.product_sku.sku_code}"

	class Meta:
		db_table = 'inventory'

	def update_stock(self, quantity, operation_type, reason=None, reference=None):
		if operation_type == OperationChoice.REMOVE.value and quantity > self.stock_quantity:
			raise ValueError("Not enough stock available.")
		previous_quantity = self.stock_quantity
		if operation_type == OperationChoice.ADD.value:
			self.stock_quantity += quantity
		elif operation_type == OperationChoice.REMOVE.value:
			self.stock_quantity -= quantity
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
		'ProductSKU', on_delete=models.CASCADE, related_name='stock_movements'
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


