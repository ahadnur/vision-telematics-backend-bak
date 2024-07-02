from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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

    @property
    def groups(self):
        return self.user_groups.all()

    def user_permissions(self):
        return self.user_permissions.all()


class Account(TimeStamp):
    # account_name and company_name same
    account_name = models.CharField(max_length=255)  # invoice account
    accounts_contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    in_add = models.CharField(max_length=255, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    install_level = models.ForeignKey('InstallLevel', on_delete=models.SET_NULL, related_name='install_level',
                                      null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    invoice_terms = models.CharField(null=True, blank=True)  # maybe days.
    opened = models.DateTimeField(null=True, blank=True)
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


class Invoice(TimeStamp):
    invoice_number = models.CharField(max_length=100)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    order = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True, blank=True)
    paid = models.BooleanField(default=False)
    payment_date = models.DateField(blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50, default='Pending')  # e.g., Pending, Paid, Overdue
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['date']),
            models.Index(fields=['customer']),
        ]


class InvoiceServiceLog(TimeStamp):
    LOG_REQ_TYPE = [('create_invoice', 'Create Invoice'),
                    ('create_customer', 'Create Customer'),
                    ('update_customer', 'Update Customer'),
                    ('other', 'Other'),]

    account_invoice = models.ForeignKey('Invoice', models.DO_NOTHING, blank=True, null=True)
    status_code = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    request_data = models.TextField(null=True, blank=True)
    response_data = models.TextField(null=True, blank=True)
    invoice_number = models.CharField(max_length=50, null=True, blank=True)  # DocumentNumber in Fortnox
    retry_count = models.IntegerField(null=False, blank=False, default=0)
    request_type = models.CharField(max_length=100, choices=LOG_REQ_TYPE, default='create_invoice',
                                    null=False, blank=False)
    customer_number = models.CharField(max_length=60, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'invoice_service_log'

    def __str__(self):
        return str(self.id)

