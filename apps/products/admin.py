from django.contrib import admin
from .models import (
    Product, Category, PO, CarData, Supplier, 
    ProductSKU, StockSuppliedTo,
    SubscriptionPlan, SubscribeAPlan,
    UsageMetrics, SubscriptionTransaction,
)


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


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'tier', 'price', 'billing_cycle']
    list_display_links = ['name']


@admin.register(SubscribeAPlan)
class SubscribeAPlanAdmin(admin.ModelAdmin):
    list_display = ['subscriber_name', 'plan_name', 'current_start_date', 'current_end_date', 'status', 'auto_renew']
    list_display_links = ['subscriber_name', 'plan_name']

    def subscriber_name(self, obj):
        return str(obj.subscriber)

    def plan_name(self, obj):
        return obj.plan.name


@admin.register(UsageMetrics)
class UsageMetricsAdmin(admin.ModelAdmin):
    list_display = ['subscriber_name', 'discount', 'discount_count', 'discount_used', 'reset_date']
    list_display_links = ['subscriber_name']

    def subscriber_name(self, obj):
        return str(obj.subscriber)


@admin.register(SubscriptionTransaction)
class SubscriptionTransactionAdmin(admin.ModelAdmin):
    list_display = ['subscriber_name', 'plan_name', 'amount_paid', 'start_date', 'end_date', 'payment_reference']
    list_display_links = ['subscriber_name', 'plan_name']

    def subscriber_name(self, obj):
        return str(obj.subscriber)

    def plan_name(self, obj):
        return obj.plan.name
