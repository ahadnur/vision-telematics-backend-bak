from rest_framework import serializers
from apps.accounts.models import Account


class AccountWriteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('account_name', 'accounts_contact_name', 'contact_number', 'in_add', 'notes',
				  'discount', 'invoice_terms', 'confirmation_email', 'freeze_account',
				  'hot_account', 'send_confirmation', 'sales_contact', 'sales_contact_number', 'sales_email')

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
		fields = ['id', 'account_name']
