from django.db import transaction, IntegrityError
from rest_framework import serializers

from apps.accounts.serializers import logger
from apps.customers.models import Customer, CustomerAddress, CustomerVehicleInfo, CustomerInstallation
from apps.utilities.models import VehicleMake, VehicleModel, VehicleType
from apps.customers.models.customer import CustomerCompany


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerCompany
        fields = ['id', 'company_name']


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerAddress
        fields = ('address_line_1', 'address_line_2', 'address_line_3', 'address_line_4', 'postcode')


class CustomerWriteSerializer(serializers.ModelSerializer):
    address = CustomerAddressSerializer()

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
            raise serializers.ValidationError({'customer_ref_number': 'This customer reference number already exists.'})
        except Exception as e:
            logger.error(f'create customer error on: {e}')
            raise serializers.ValidationError("Failed to create customer and address.")

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)  # Pop address data if it exists
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        try:
            with transaction.atomic():
                instance.save()  # Save changes to the Customer instance

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
        fields = ['id', 'customer_ref_number', 'contact_name', 'phone_numbers', 'email_address', 'company', 'address']


class CustomerVehicleSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.objects.all())
    vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
    vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

    class Meta:
        model = CustomerVehicleInfo
        fields = ['customer', 'registration_number', 'vehicle_make', 'vehicle_model', 'vehicle_type']


# for oder
class CustomerOrderOptionsSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = CustomerInstallation
        fields = ['customer', 'job_required', 'preferred_install_date', 'kit_installed']


class CustomerVehicleInfoSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    vehicle_make = serializers.PrimaryKeyRelatedField(queryset=VehicleMake.objects.all())
    vehicle_model = serializers.PrimaryKeyRelatedField(queryset=VehicleModel.objects.all())
    vehicle_type = serializers.PrimaryKeyRelatedField(queryset=VehicleType.objects.all())

    class Meta:
        model = CustomerVehicleInfo
        fields = ['customer', 'vehicle_make', 'vehicle_model', 'vehicle_type', 'registration_number']
