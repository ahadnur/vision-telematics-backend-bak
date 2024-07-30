from django.db import models
from apps.utilities.models import TimeStamp


class NotifiedBy(TimeStamp):
    notified_by = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.notified_by