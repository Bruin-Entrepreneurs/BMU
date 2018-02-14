from django.db import models
from apps.user.models import User 
# Create your models here.


class Events(models.Model):
    
    name = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=255, null=True)
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=150, null=True)

    def get_name(self):
        return 'Event Name: '+  self.name
    def __str__(self):
        return self.name
