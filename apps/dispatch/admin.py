from django.contrib import admin
from apps.dispatch.models import Dispatch, DeliveryRoute

admin.site.register(Dispatch)
admin.site.register(DeliveryRoute)
