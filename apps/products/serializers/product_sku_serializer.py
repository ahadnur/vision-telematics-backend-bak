from rest_framework import serializers

from apps.products.models import ProductSKU


class GetProductSKUByProductIDSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    class Meta:
        model = ProductSKU
        fields = [
            'id',
            'product_name',
            'sku_code',
            'description',
            'unit_price',
            'qty',
            'discount',
            'suppliers',
        ]
        read_only_fields = (
            'id',
            'sku_code',
            'description',
            'discount',
            'unit_price',
        )

    def get_product_name(self, obj):
        return obj.product.product_name