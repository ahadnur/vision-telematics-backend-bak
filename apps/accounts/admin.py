from django.contrib import admin
from .models import Account, User, UserRole, Profile, AuditTrail, NotifiedBy, Bulletin, Staff, InstallLevel


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'id', 'accounts_contact_name')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')


admin.site.register(AuditTrail)
admin.site.register(NotifiedBy)
admin.site.register(Bulletin)
admin.site.register(Staff)
admin.site.register(InstallLevel)

