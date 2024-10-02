from itertools import product

from rest_framework import serializers
from django.db import transaction
from apps.products.models import Category, ProductSKU, Product


class ProductSKUSerializer(serializers.ModelSerializer):
	product = serializers.PrimaryKeyRelatedField(
		queryset=Product.objects.filter(is_active=True),
	)

	class Meta:
		model = ProductSKU
		fields = ['id', 'sku_code', 'description', 'unit_price', 'qty', 'discount', 'total', 'product']


class ProductSerializer(serializers.ModelSerializer):
	category = serializers.PrimaryKeyRelatedField(
		queryset=Category.objects.filter(is_active=True)
	)
	product_skus = ProductSKUSerializer(many=True, required=False)

	class Meta:
		model = Product
		fields = ['id', 'product_name', 'description', 'cost', 'note', 'category', 'product_skus']

	def create(self, validated_data):
		product_skus_data = validated_data.pop('product_skus')
		with transaction.atomic():
			_product = Product.objects.create(**validated_data)
			product_skus = [
				ProductSKU(product=_product, **sku_data) for sku_data in product_skus_data
			]
			ProductSKU.objects.bulk_create(product_skus)
		return product