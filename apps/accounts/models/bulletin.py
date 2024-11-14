from django.db import models

from apps.common.active_manager import ActiveManager
from apps.utilities.models import BaseModel


class Bulletin(BaseModel):
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    date = models.DateField(blank=True, null=True)
    published = models.BooleanField(default=False)
    bulletin = models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.subject}"