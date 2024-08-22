from django.contrib import admin
from .models import Product, Category, PO, CarData, Supplier, ProductSKU, StockSuppliedTo, StockControlCode

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(PO)
admin.site.register(CarData)
admin.site.register(Supplier)
admin.site.register(StockSuppliedTo)


# admin.site.register(StockControlCode)


class ProductSKUAdmin(admin.ModelAdmin):
    exclude = ('total',)
    list_display = ('product_name', 'description', 'unit_price', 'total')

    def product_name(self, obj):
        return obj.product.product_name


admin.site.register(ProductSKU, ProductSKUAdmin)
