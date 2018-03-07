from django.conf.urls import url
from apps.event.views import EventCreate

urlpatterns = [
    url(r'^$', EventCreate.as_view(), name='event_create')
]

