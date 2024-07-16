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


class UserRole(TimeStamp):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, TimeStamp):
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

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.email


# In lagacy system this is a staff
class Staff(TimeStamp):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Account(TimeStamp):
    # account_name and company_name same
    account_name = models.CharField(max_length=255)  # invoice account
    accounts_contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    in_add = models.CharField(max_length=255, null=True, blank=True)
    post_code = models.CharField(max_length=20, null=True, blank=True)
    install_level = models.ForeignKey('InstallLevel', related_name='install_levels',
                                      on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    invoice_terms = models.CharField(max_length=50, null=True, blank=True,)  # maybe days.
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


class NotifiedBy(models.Model):
    notified_by = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.notified_by


class InstallLevel(models.Model):
    install_level = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.install_level


class Bulletin(TimeStamp):
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    date = models.DateField(blank=True, null=True)
    published = models.BooleanField(default=False)
    bulletin = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.subject}"


class AuditTrail(models.Model):
    """Track who responsible for certain action"""
    ACTION_CHOICES = (
        ('INSERT', 'Insert'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    actioned_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    table_name = models.CharField(max_length=100)
    record_id = models.IntegerField()
    details = models.TextField()

    def __str__(self):
        return f'{self.timestamp} - {self.user} - {self.action} - {self.table_name}'

    class Meta:
        verbose_name = 'Audit Trail'
        verbose_name_plural = 'Audit Trail'
