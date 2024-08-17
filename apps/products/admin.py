from django.contrib import admin
from apps.products.models import Product, Category, PO, CarData, Supplier, PasteError, StockSuppliedTo, StockControlCode

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(PO)
admin.site.register(CarData)
admin.site.register(Supplier)
admin.site.register(StockSuppliedTo)
admin.site.register(StockControlCode)
admin.site.register(PasteError)
