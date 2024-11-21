from rest_framework import serializers
from apps.customers.models.customer import CustomerCompany


class CompanyListSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerCompany
		fields = ['id', 'company_name']
