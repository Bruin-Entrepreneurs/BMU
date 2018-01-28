from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser as _DjangoAbstractUser


# DONT WORRY ABOUT THIS - THIS IS DJANGO MAGIC WE CAN HAVE A CUSTOM AUTH USER
class AbstractUser(_DjangoAbstractUser):
    class Meta:
        abstract = True

# Need to do this after the class object is created, because we need _meta access
AbstractUser._meta.get_field('groups').rel.related_name = 'special_users'
AbstractUser._meta.get_field('groups').rel.related_query_name = 'special_users'

AbstractUser._meta.get_field('user_permissions').rel.related_name = 'special_users'
AbstractUser._meta.get_field('user_permissions').rel.related_query_name = 'special_users'


class User(AbstractUser):
    """
    Model representing a User who can create and join events
    """
    username = models.CharField(max_length=50, db_index=True, unique=True, null=True, blank=True)
    name = models.CharField(max_length=50)
    display_name = models.CharField(max_length=100, default='')
    bio = models.CharField(max_length=500, blank=True, default='')
    status = models.BooleanField()

    # events = models.ManyToManyField('event.events', on_delete=models.SET_NULL, related_name='events', null=True)
