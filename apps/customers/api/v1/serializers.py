from rest_framework import serializers

from apps.accounts.models import Account
from apps.customers.models import Customer
from apps.utilities.models import Company


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name']


# class OrderCustomerSerializer(serializers.Serializer):
#     customer_ref_number = serializers.CharField(max_length=100)
#     contact_name = serializers.CharField(max_length=100)
#     company = serializers.CharField(max_length=100)
#     phone_numbers = serializers.ListField(child=serializers.CharField(max_length=15))
#     email_address = serializers.EmailField()
#     is_hot = serializers.BooleanField()
#     install_address_2 = serializers.CharField(max_length=255, required=False)
#     install_address_3 = serializers.CharField(max_length=255, required=False)
#     install_address_4 = serializers.CharField(max_length=255, required=False)
#     delivery_address_2 = serializers.CharField(max_length=255, required=False)
#     delivery_address_3 = serializers.CharField(max_length=255, required=False)
#     delivery_address_4 = serializers.CharField(max_length=255, required=False)
#     vehicle_make = serializers.CharField(max_length=255, required=False)
#     vehicle_model = serializers.CharField(max_length=255, required=False)
#     phone_make = serializers.CharField(max_length=255, required=False)
#     phone_model = serializers.CharField(max_length=255, required=False)
#     existing_kit = serializers.CharField(max_length=255, required=False)
#     requested_by = serializers.CharField(max_length=255, required=False)
#     po_number_kit = serializers.CharField(max_length=255, required=False)
#     vehicle_type = serializers.PrimaryKeyRelatedField()
#     registration_number = serializers.CharField(max_length=255, required=False)
#     account = serializers.PrimaryKeyRelatedField()

# class OrderAccountSerializer(serializers.Serializer):
#     account_name = serializers.CharField(max_length=100)
#     in_address = serializers.CharField(max_length=100, required=False)


class OrderWriteSerializer(serializers.Serializer):
    # customer_data = OrderCustomerSerializer()
    pass
    # account_data = OrderAccountSerializer()

    # def create(self, validated_data):
    #     # Extract the nested data
    #     customer_data = validated_data.pop('customer_data')
    #     account_data = validated_data.pop('account_data')
    #
    #     # Perform custom logic, like creating objects in the database
    #     customer = Customer.objects.create(**customer_data)
    #     account = Account.objects.create(**account_data)
    #
    #     return {
    #         'customer': customer,
    #         'account': account
    #     }
