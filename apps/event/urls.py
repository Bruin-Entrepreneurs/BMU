from django.conf.urls import url
from apps.event.views import EventListCreateView, EventTypeListView, EventDetailView, EventAcceptView, EventDeclineView

urlpatterns = [
    url(r'^types/?$', EventTypeListView.as_view(), name='event_types'),
    url(r'^$', EventListCreateView.as_view(), name='events'),
    url(r'^personal_events/$', EventDetailView.as_view(), name='personal_events')
    url(r'^(?P<event_id>\d+)/?$', EventDetailView.as_view(), name='event_detail'),
    url(r'^(?P<event_id>\d+)/accept/?$', EventAcceptView.as_view(), name='event_accept'),
    url(r'^(?P<event_id>\d+)/decline/?$', EventDeclineView.as_view(), name='event_decline'),
]
