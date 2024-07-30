from django.db import models
from .models import TimeStamp


# In lagacy system this is a staff
class Staff(TimeStamp):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name