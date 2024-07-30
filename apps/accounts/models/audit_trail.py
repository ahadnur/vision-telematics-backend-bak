from django.db import models
from apps.utilities.models import TimeStamp


class AuditTrail(TimeStamp):
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
