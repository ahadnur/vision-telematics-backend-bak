from django.contrib import admin
from .models import Account, User, UserRole, Profile


# from .models


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')


admin.site.register(Account)
