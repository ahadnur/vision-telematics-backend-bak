from rest_framework import serializers
from apps.inventory.models import StockMovement, Inventory, StockThreshold
from apps.products.models import ProductSKU
from apps.common.enums import OperationChoice


class InventorySerializer(serializers.ModelSerializer):
    product_sku = serializers.PrimaryKeyRelatedField(queryset=ProductSKU.objects.all())
    product_name = serializers.CharField(source='product_sku.product.product_name', read_only=True)
    sku_code = serializers.CharField(source='product_sku.sku_code', read_only=True)
    unit_price = serializers.DecimalField(source='product_sku.unit_price', max_digits=10, decimal_places=2, read_only=True)
    is_low_stock = serializers.SerializerMethodField()


    class Meta:
        model = Inventory
        fields = ['id', 'product_sku', 'product_name', 'sku_code', 'unit_price', 'stock_quantity', 'is_low_stock']

    def get_is_low_stock(self, obj):
        threshold = StockThreshold.objects.first()
        if threshold:
            return obj.stock_quantity < threshold.min_quantity
        return False


class InventoryCreateSerializer(serializers.ModelSerializer):
    product_sku = serializers.PrimaryKeyRelatedField(queryset=ProductSKU.objects.all())
    
    class Meta:
        model = Inventory
        fields = ['product_sku', 'stock_quantity']

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
    
    def validate_product_sku(self, value):
        if Inventory.active_objects.filter(product_sku=value).exists():
            raise serializers.ValidationError("Inventory already exists for this product.")
        return value


class InventoryUpdateSerializer(serializers.Serializer):
    product_sku = serializers.PrimaryKeyRelatedField(queryset=ProductSKU.active_objects.all())
    quantity = serializers.IntegerField(min_value=1)
    operation_type = serializers.ChoiceField(choices=[
        (OperationChoice.ADD.value, 'Add'),
        (OperationChoice.REMOVE.value, 'Remove'),
        (OperationChoice.ADJUST.value, 'Adjust')
    ])
    reason = serializers.CharField(required=False, allow_blank=True)
    reference = serializers.CharField(required=False, allow_blank=True)

    def validate_product_sku(self, value):
        if Inventory.active_objects.filter(product_sku=value).exists():
            return value
        raise serializers.ValidationError("Inventory does not exist for this product.")


class InventoryDestroySerializer(serializers.Serializer):
    product_sku = serializers.PrimaryKeyRelatedField(queryset=ProductSKU.active_objects.all())

    def validate_product_sku(self, value):
        if Inventory.active_objects.filter(product_sku=value).exists():
            return value
        raise serializers.ValidationError("Inventory does not exist for this product.")


class StockMovementSerializer(serializers.ModelSerializer):
    product_sku = serializers.PrimaryKeyRelatedField(queryset=ProductSKU.objects.all())
    inventory = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all())
    sku_code = serializers.CharField(source='product_sku.sku_code', read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            'id', 'product_sku', 'sku_code', 'inventory', 'operation_type',
            'quantity', 'previous_quantity', 'new_quantity', 'reason', 'reference', 'created_at'
        ]


class UpdateStockMovementSerializer(serializers.Serializer):
    product_sku = serializers.PrimaryKeyRelatedField(queryset=ProductSKU.objects.all())
    quantity = serializers.IntegerField()
    operation_type = serializers.ChoiceField(choices=OperationChoice.choices)
    reason = serializers.CharField(required=False, allow_blank=True)
    reference = serializers.CharField(required=False, allow_blank=True)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


class StockThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockThreshold
        fields = ['min_quantity']