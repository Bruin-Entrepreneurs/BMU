from django.conf.urls import url
from apps.event.views import EventListCreateView, EventTypeListView, EventDetailView

urlpatterns = [
    url(r'^$', EventListCreateView.as_view(), name='events'),
    url(r'^(?P<event_id>\d+)/?$', EventDetailView.as_view(), name='event_detail'),
    url(r'^types/?$', EventTypeListView.as_view(), name='event_types'),
]
