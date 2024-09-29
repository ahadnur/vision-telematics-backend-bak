from django.contrib import admin
from apps.engineers.models import Engineer, EngineerInvoice, EngineerCompany


@admin.register(EngineerCompany)
class EngineerCompanyAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']
	fields = ['name']


admin.site.register(Engineer)
admin.site.register(EngineerInvoice)
