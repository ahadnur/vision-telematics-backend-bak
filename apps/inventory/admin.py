from django.contrib import admin
from apps.inventory.models import Inventory, StockMovement


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product_sku', 'stock_quantity')
    search_fields = ('product_sku__sku_code',)


class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product_sku', 'operation_type', 'reason', 'quantity', 'created_at')
    search_fields = ('product_sku__sku_code', 'operation_type')


admin.site.register(Inventory, InventoryAdmin)
admin.site.register(StockMovement, StockMovementAdmin)