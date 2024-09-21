from datetime import datetime, timedelta

import jwt
from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from apps.utilities.models import TimeStamp


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        if not kwargs.get('email', None):
            raise ValueError('Email must be specified!')
        if not kwargs.get('user_type_id', None):
            raise ValueError('User type must be specified!')

        with transaction.atomic():
            user = self.model(
                email=self.normalize_email(kwargs['email']),
                user_type_id=kwargs['user_type_id'],
            )
            user.set_password(kwargs['password'])
            user.is_active = True
            user.save()

            first_name = kwargs['first_name']
            last_name = kwargs['last_name']
            Profile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name
            )
        return user

    def create_superuser(self, email: str, password: str, user_type: str):
        """
        Create superuser method
        """
        if not email:
            raise ValueError('Email must be specified!')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.user_type = user_type
        user.set_password(password)
        user.save()
        return user


class UserRole(TimeStamp):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin, TimeStamp):
    """Custom user model"""
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True)
    email_verfication_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def token(self, secret_key):
        return self._generate_jwt_token(secret_key=secret_key)

    def _generate_jwt_token(self, secret_key):
        iat_dt = datetime.utcnow()
        exp_dt = iat_dt + timedelta(days=1)
        token = jwt.encode({
            'user_id': self.id,
            'user_type': self.user_type_id,
            'exp': int(exp_dt.timestamp()),
            'iat': int(iat_dt.timestamp()),
        }, secret_key, algorithm='HS256')
        return token

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email'),
        ]


class Profile(TimeStamp):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)

    @property
    def name(self):
        return ' '.join(filter(bool, [self.first_name, self.last_name]))

    def __str__(self):
        return ' '.join(filter(bool, [self.first_name, self.last_name]))

    class Meta:
        db_table = 'profile'
