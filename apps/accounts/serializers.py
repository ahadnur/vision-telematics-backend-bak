from rest_framework import serializers
from apps.accounts.models import Account, User, UserRole
from apps.accounts.services import UserService
import logging

logger = logging.getLogger(__name__)


class UserWriteSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.userserive = UserService()

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(allow_empty=False, many=True, queryset=UserRole.objects.all())

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'role')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = User(email=validated_data['email'])
        user.is_active = True
        user.set_password(password)
        user.save()

        if 'role' in validated_data:
            user.role.set(validated_data['role'])

        return user

    def to_internal_value(self, data):
        if isinstance(data.get('role'), int):
            data['role'] = [data['role']]
        return super().to_internal_value(data)


class ResetPasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def update(self, instance, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        instance.set_password(password)
        instance.save()
        return instance


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role')


class AccountWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_name', 'contact_number', 'in_add', 'notes', 'discount',
                  'invoice_terms', 'opened_by', 'confirmation_email', 'freeze_account', 'hot_account',
                  'send_confirmation', 'sales_contact', 'sales_contact_number', 'sales_email')

    def create(self, validated_data):
        account = Account.objects.create(**validated_data)
        return account

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name']
