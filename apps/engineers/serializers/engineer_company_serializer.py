from rest_framework import serializers

from apps.accounts.models import Company


class EngineerCompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name']

