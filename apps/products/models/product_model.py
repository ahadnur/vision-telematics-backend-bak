from django.db import models
from apps.utilities.models import BaseModel


class Category(BaseModel):
	category_name = models.CharField(max_length=255, null=True, blank=True)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.category_name


class Product(BaseModel):
	product_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
	description = models.TextField(null=True, blank=True)
	note = models.TextField(null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, db_index=True)

	def __str__(self):
		return f'{self.product_name}'


# PastError
class ProductSKU(BaseModel):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_skus', null=True, blank=True)
	sku_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
	description = models.TextField(blank=True, null=True)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	qty = models.IntegerField(blank=True, null=True)
	discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

	'''
	Multiple Suppliers per SKU: A single SKU can be supplied by different suppliers.
	Multiple SKUs per Supplier: A single supplier can offer multiple SKUs.
	'''
	suppliers = models.ManyToManyField(
		'products.Supplier', 
		related_name='product_skus', 
		blank=True
	)


	class Meta:
		verbose_name_plural = 'ProductSKUs'

	def __str__(self):
		return f"{self.product.product_name}-{self.sku_code}"

	def save(self, *args, **kwargs):
		if self.unit_price is not None and self.qty is not None:
			self.total = self.unit_price * self.qty
		else:
			self.total = None
		super(ProductSKU, self).save(*args, **kwargs)


