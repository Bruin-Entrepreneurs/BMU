from django.db import models
from django.utils import timezone


class EventType(models.Model):
    name = models.CharField(max_length=150, null=False, unique=True, db_index=True)
    image_url = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.name


class Event(models.Model):
    creator = models.ForeignKey('user.User', on_delete=models.SET_NULL, related_name="creator", null=False)
    event_type = models.ForeignKey('event.EventType', on_delete=models.SET_NULL, related_name="event_type", null=False)
    accepted = models.ManyToManyField('user.User', related_name="accepted")
    declined = models.ManyToManyField('user.User', related_name="declined")
    super_invited = models.ManyToManyField('user.User', related_name="super_invited")
    description = models.CharField(max_length=255, blank=True, default='')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1))

    def __str__(self):
        return "{} at {}".format(self.event_type.name, self.start_time)
