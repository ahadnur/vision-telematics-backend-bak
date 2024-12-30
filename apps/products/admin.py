from django.contrib import admin
from .models import Product, Category, PO, CarData, Supplier, ProductSKU, StockSuppliedTo, Inventory


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'id')


admin.site.register(Category)
admin.site.register(PO)
admin.site.register(CarData)
admin.site.register(Supplier)
admin.site.register(StockSuppliedTo)


class ProductSKUAdmin(admin.ModelAdmin):
    exclude = ('total',)
    list_display = ('product_name', 'sku_code', 'id', 'description', 'unit_price', 'total')

    def product_name(self, obj):
        return obj.product.product_name


admin.site.register(ProductSKU, ProductSKUAdmin)

admin.site.register(Inventory)