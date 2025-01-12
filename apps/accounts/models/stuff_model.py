from django.db import models
from apps.utilities.models import BaseModel


# In legacy system this is a staff
class Staff(BaseModel):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'staff'
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name