from rest_framework import serializers

from apps.accounts.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id',
            'company_name',
            'registration_number',
            'primary_contact_name',
            'primary_contact_email',
            'primary_contact_phone',
            'address',
            'postal_code',
            'notes',
            'is_engineer_company'
        ]