from django.db import models
from apps.utilities.models import BaseModel


class NotifiedBy(BaseModel):
    notified_by = models.ForeignKey('User', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        db_table = 'notified_by'
        ordering = ['-created_at']

    def __str__(self):
        return self.notified_by