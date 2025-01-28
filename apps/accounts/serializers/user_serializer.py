from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from apps.accounts.backends import CustomAuthBackend
from apps.accounts.models import Account, User, UserRole
import logging

logger = logging.getLogger(__name__)


class UserWriteSerializer(serializers.Serializer):
	first_name = serializers.CharField(write_only=True)
	last_name = serializers.CharField(write_only=True)
	email = serializers.EmailField(write_only=True, required=False)
	password = serializers.CharField(write_only=True, required=False)
	user_type = serializers.PrimaryKeyRelatedField(queryset=UserRole.active_objects.all())

	def validate(self, data):
		if self.instance:
			if 'email' in data and self.instance.email != data['email']:
				if User.objects.filter(email=data['email']).exists():
					raise serializers.ValidationError("A user with this email already exists.")
		else:
			if 'email' in data and User.objects.filter(email=data['email']).exists():
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

	def update(self, instance, validated_data):
		with transaction.atomic():
			instance.email = validated_data.get('email', instance.email)
			instance.user_type = validated_data.get('user_type', instance.user_type)
			if 'password' in validated_data:
				instance.set_password(validated_data['password'])
			instance.save()
			profile = instance.profile
			profile.first_name = validated_data.get('first_name', profile.first_name)
			profile.last_name = validated_data.get('last_name', profile.last_name)
			profile.save()
		return instance


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

