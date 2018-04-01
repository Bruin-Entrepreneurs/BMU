from django.conf.urls import url
from apps.event.views import EventListCreateView, EventTypeListView

urlpatterns = [
    url(r'^$', EventListCreateView.as_view(), name='events'),
    url(r'^types/?$', EventTypeListView.as_view(), name='event_typess'),
]

