from django.contrib import admin
from .models import Account, User, UserRole

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(Account)