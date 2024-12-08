from apps.common.enums import OperationChoice
from apps.products.models import Inventory


class InventoryService:
	@staticmethod
	def add_stock(product_sku, quantity, reason=None, reference=None):
		inventory = Inventory.objects.get(product_sku=product_sku)
		inventory.update_stock(quantity, OperationChoice.ADD.value, reason, reference)

	@staticmethod
	def remove_stock(product_sku, quantity, reason=None, reference=None):
		inventory = Inventory.objects.get(product_sku=product_sku)
		inventory.update_stock(quantity, OperationChoice.REMOVE.value, reason, reference)

	@staticmethod
	def adjust_stock(product_sku, new_quantity, reason=None):
		inventory = Inventory.objects.get(product_sku=product_sku)
		inventory.update_stock(new_quantity, OperationChoice.ADJUST.value, reason)
