from rest_framework import serializers
from apps.accounts.models import Account, User


class UserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'name')


class AccountWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_name', 'contact_number', 'in_add', 'notes', 'discount',
                  'invoice_terms', 'opened', 'opened_by', 'confirmation_email',
                  'send_confirmation', 'sales_contact', 'sales_contact_number', 'sales_email')

    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        return account

    def update(self, instance, validated_data):
        # pass
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

