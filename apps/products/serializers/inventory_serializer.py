from rest_framework import serializers
from apps.products.models import Inventory, StockMovement, Product


class InventorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Inventory
		fields = ['id', 'product_sku', 'stock_quantity']


class StockMovementSerializer(serializers.ModelSerializer):
	class Meta:
		model = StockMovement
		fields = [
			'id', 'product_sku', 'inventory', 'operation_type',
			'quantity', 'previous_quantity', 'new_quantity',
			'reason', 'reference', 'created_at'
		]


class UpdateStockMovementSerializer(serializers.ModelSerializer):

	class Meta:
		model = StockMovement
		fields = ['product_sku', 'quantity', 'operation_type', 'reason', 'reference', 'created_at']
