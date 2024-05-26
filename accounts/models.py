from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ulilities.models import TimeStamp


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
        user.save(self._db)
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
        user.set_password(password)
        user.save(self._db)
        return user


class User(AbstractBaseUser, TimeStamp):
    """Custom user model"""
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email


class InvoiceAccount(TimeStamp):
    account_name = models.CharField(max_length=255)  # invoice account
    accounts_contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    fax_number = models.CharField(max_length=20, null=True, blank=True)
    in_add = models.CharField(max_length=255, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    install_level = models.ForeignKey('InstallLevel', on_delete=models.SET_NULL, related_name='install_level',
                                      null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    invoice_terms = models.CharField(null=True, blank=True)
    opened = models.DateField(null=True, blank=True)
    opened_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    freeze_account = models.BooleanField(default=False)
    hot_account = models.BooleanField(default=False)
    reseller_account = models.BooleanField(default=False)
    confirmation_email = models.EmailField(max_length=100, null=True, blank=True)
    send_confirmation = models.BooleanField(default=False)

    sales_contact = models.CharField(max_length=100, null=True, blank=True)
    sales_contact_number = models.CharField(max_length=20, null=True, blank=True)
    sales_email = models.EmailField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.account_name
