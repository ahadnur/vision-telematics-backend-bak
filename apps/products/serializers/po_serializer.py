from rest_framework import serializers
from apps.products.models import PO, Supplier, ProductSKU
from apps.products.serializers import SupplierSerializer, ProductSKUSerializer


class POListSerializer(serializers.ModelSerializer):
	supplier = SupplierSerializer(read_only=True)
	product_sku = ProductSKUSerializer(read_only=True)

	class Meta:
		model = PO
		fields = [
			'id',
			'po_ref',
			'invoice_number',
			'date',
			'supplier',
			'product_sku',
			'item_ordered',
			'received',
			'qty',
		]


class POCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = PO
		fields = [
			'po_ref',
			'invoice_number',
			'date',
			'description',
			'supplier',
			'product_sku',
			'item_ordered',
			'received',
			'qty',
		]


class PORetrieveSerializer(serializers.ModelSerializer):
	supplier = SupplierSerializer(read_only=True)
	product_sku = ProductSKUSerializer(read_only=True)

	class Meta:
		model = PO
		fields = [
			'id',
			'po_ref',
			'invoice_number',
			'date',
			'description',
			'supplier',
			'product_sku',
			'item_ordered',
			'received',
			'qty',
		]


class POUpdateSerializer(serializers.ModelSerializer):
	class Meta:
		model = PO
		fields = [
			'invoice_number',
			'date',
			'description',
			'supplier',
			'product_sku',
			'item_ordered',
			'received',
			'qty',
		]