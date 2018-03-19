from django.db import models
from django.utils import timezone


class EventType(models.Model):
    name = models.CharField(max_length=150, null=True)
    # image = models.ImageField()

    def __str__(self):
        return self.name


class Event(models.Model):
    creator = models.OneToOneField('user.User', related_name="creator", null=False)
    event_type = models.ForeignKey('event.EventType', related_name="event_type", null=False)
    accepted = models.ManyToManyField('user.User', related_name="accepted")
    declined = models.ManyToManyField('user.User', related_name="declined")
    super_invited = models.ManyToManyField('user.User', related_name="super_invited")
    description = models.CharField(max_length=255, blank=True, default='')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1))

    def __str__(self):
        return "%s at %s".format(self.event_type, self.start_time)
