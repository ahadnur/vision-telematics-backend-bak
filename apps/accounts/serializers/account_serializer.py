from rest_framework import serializers
from apps.accounts.models import Account, Company
from apps.customers.models import Customer


class AccountWriteSerializer(serializers.ModelSerializer):
	owner_company = serializers.PrimaryKeyRelatedField(required=False, queryset=Company.objects.all())
	owner_customer = serializers.PrimaryKeyRelatedField(required=False, queryset=Customer.objects.all())

	class Meta:
		model = Account
		fields = ('account_contact', 'account_number', 'account_type', 'owner_company',
				  'discount', 'invoice_terms', 'confirmation_email', 'freeze_account',
				  'hot_account', 'send_confirmation', 'owner_customer')

	def create(self, validated_data):
		account = Account.objects.create(**validated_data)
		return account

	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()
		return instance


class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = "__all__"


class AccountListDropdownSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ['id', 'account_contact']
