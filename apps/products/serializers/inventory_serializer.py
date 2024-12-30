from rest_framework import serializers
from apps.products.models import Inventory, StockMovement, Product


class InventorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField(max_length=255)
    quantity = serializers.IntegerField()
    sku_code = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)



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
