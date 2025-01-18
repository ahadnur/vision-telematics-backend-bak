import logging

from django.db import transaction, IntegrityError
from rest_framework import serializers

from apps.accounts.models import Account, Company
from apps.customers.models import Customer, CustomerAddress, CustomerVehicleInfo

logger = logging.getLogger(__name__)


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ('address_line_1', 'address_line_2', 'address_line_3', 'address_line_4', 'postcode')


class CustomerWriteSerializer(serializers.ModelSerializer):
    address = CustomerAddressSerializer()
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all())

    class Meta:
        model = Customer
        fields = ['id', 'customer_ref_number', 'contact_name', 'phone_numbers', 'email_address', 'company', 'address']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        try:
            with transaction.atomic():
                customer = Customer.objects.create(**validated_data)
                CustomerAddress.objects.create(customer=customer, **address_data)
            return customer
        except IntegrityError as e:
            logger.error(e)
            raise serializers.ValidationError({'customer_ref_number': 'This customer reference number already exists.'})
        except Exception as e:
            logger.error(f'create customer error on: {e}')
            raise serializers.ValidationError("Failed to create customer and address.")

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            with transaction.atomic():
                instance.save()
                if address_data:
                    customer_address, created = CustomerAddress.objects.get_or_create(customer=instance)
                    for attr, value in address_data.items():
                        setattr(customer_address, attr, value)
                    customer_address.save()
            return instance
        except IntegrityError:
            raise serializers.ValidationError({'customer_ref_number': 'This customer reference number already exists.'})
        except Exception as e:
            logger.error(f'update customer error on: {e}')
            raise serializers.ValidationError("Failed to update customer and address.")


class GetCustomerSerializer(serializers.ModelSerializer):
    address = CustomerAddressSerializer(source='customeraddress')

    class Meta:
        model = Customer
        fields = ['id', 'customer_ref_number', 'contact_name', 'phone_numbers', 'email_address',  'address']


class CustomerDropdownSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id', 'contact_name']

