from django.contrib import admin
from .models import (InstallType, CreditReason, CallBackReason, CallBackReasonOld, PaymentMethod,
                     ContactHistoryReason, POSupplierRef, ContactHistoryStatus)

admin.site.register(InstallType)
admin.site.register(CreditReason)
admin.site.register(CallBackReason)
admin.site.register(CallBackReasonOld)
admin.site.register(PaymentMethod)
admin.site.register(ContactHistoryReason)
admin.site.register(POSupplierRef)
admin.site.register(ContactHistoryStatus)
