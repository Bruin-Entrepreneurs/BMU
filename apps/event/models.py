from django.db import models
from django.utils import timezone


class EventType(models.Model):
    name = models.CharField(max_length=150, null=True)
    # image = models.ImageField()


class Event(models.Model):
    creator = models.ForeignKey('user.User', related_name="creator", null=False)
    event_type = models.ForeignKey('event.EventType', related_name="activity_type", null=False)
    accepted = models.ManyToManyField('user.User', null=True)
    super_invited = models.ManyToManyField('user.User', null=True)
    description = models.CharField(max_length=255, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1))

    def __str__(self):
        return ""
