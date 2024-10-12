from rest_framework import serializers

from apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id', 'category_name', 'is_active']

