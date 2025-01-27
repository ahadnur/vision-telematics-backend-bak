from rest_framework import serializers

from apps.accounts.models import UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'name']