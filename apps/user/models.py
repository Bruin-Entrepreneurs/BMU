from django.db import models
from django.contrib.auth.models import AbstractUser as _DjangoAbstractUser


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
    Model representing a User who can create and join event
    """
    username = models.CharField(max_length=50, db_index=True, unique=True, default='')
    bio = models.CharField(max_length=500, blank=True, default='')
    profile_pic_url = models.CharField(max_length=100, blank=True, default='')
    facebook_id = models.CharField(max_length=50, blank=True, unique=True, default='')
    notification_token = models.CharField(max_length=50, blank=True, default='')

    def __str__(self):
        return self.username
