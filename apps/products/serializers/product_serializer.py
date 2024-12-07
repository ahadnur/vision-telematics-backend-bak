from rest_framework import serializers
from django.db import transaction
from apps.products.models import Category, ProductSKU, Product, Inventory


class ProductSKUSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	product = serializers.PrimaryKeyRelatedField(
		queryset=Product.objects.filter(is_active=True),
		required=False,
	)
	sku_code = serializers.CharField(required=True)
	description = serializers.CharField()
	unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
	qty = serializers.IntegerField()
	discount = serializers.DecimalField(max_digits=10, decimal_places=2)
	total = serializers.DecimalField(max_digits=10, decimal_places=2)


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
		product_skus = []
		inventories = []

		with transaction.atomic():
			_product = Product.objects.create(**validated_data)
			for sku_data in product_skus_data:
				product_sku = ProductSKU(product=_product, **sku_data)
				product_skus.append(product_sku)

				inventory = Inventory(product_sku=product_sku, stock_quantity=sku_data.get('qty', 0))
				inventories.append(inventory)

			ProductSKU.objects.bulk_create(product_skus)
			Inventory.objects.bulk_create(inventories)
		return _product

	def update(self, instance, validated_data):
		product_skus_data = validated_data.pop('product_skus')
		with transaction.atomic():
			for key, value in validated_data.items():
				setattr(instance, key, value)
			instance.save()
			existing_skus = {sku.id: sku for sku in instance.product_skus.filter(is_active=True, is_deleted=False)}
			updated_sku_ids = set()
			existing_inventories = {inventory.product_sku.id: inventory for inventory in Inventory.objects.filter(product_sku__in=existing_skus.values())}

			for sku_data in product_skus_data:
				sku_id = sku_data.get('id')
				sku_qty = sku_data.get('qty', 0)
				if sku_id and sku_id in existing_skus:
					sku = existing_skus[sku_id]
					for key, value in sku_data.items():
						setattr(sku, key, value)
					sku.save()
					inventory = existing_inventories.get(sku.id)
					if inventory:
						inventory.stock_quantity = sku_qty  # Update stock quantity
						inventory.save()

					updated_sku_ids.add(sku_id)
				else:
					sku = ProductSKU.objects.create(product=instance, **sku_data)
					updated_sku_ids.add(sku.id)
					Inventory.objects.create(product_sku=sku, stock_quantity=sku_qty)
			skus_to_delete = set(existing_skus.keys()) - updated_sku_ids
			if skus_to_delete:
				instance.product_skus.filter(id__in=skus_to_delete).update(is_active=False, is_deleted=True)
				Inventory.objects.filter(product_sku__in=existing_skus.values()).filter(product_sku__id__in=skus_to_delete).update(is_active=False, is_deleted=True)
		return instance



