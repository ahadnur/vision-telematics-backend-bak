from django.conf import settings
from rest_framework import serializers
from apps.accounts.backends import CustomAuthBackend
from apps.accounts.models import Account, User, UserRole
import logging

logger = logging.getLogger(__name__)


class UserWriteSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    user_type = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all())

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.save()
        return user


class AuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        user = CustomAuthBackend().authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        data = {
            'email': user.email,
            'user_id': user.id,
            'user_type': user.user_type.id,
            'token': user.token(secret_key=settings.JWT_TOKEN),
        }
        return data


class ResetPasswordSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance


class GetUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='profile.first_name', default='', read_only=True)
    last_name = serializers.CharField(source='profile.last_name', default='', read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'user_type'
        ]


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
