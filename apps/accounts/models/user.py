from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from apps.utilities.models import TimeStamp


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str):
        """
        Create general user method
        """
        if not email:
            raise ValueError('Email must be specified!')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str):
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
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ManyToManyField('UserRole')
    email_verfication_code = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email


class Profile(TimeStamp):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'