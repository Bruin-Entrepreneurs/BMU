from django.conf.urls import url
from apps.event.views import EventListCreateView, EventTypeListView

urlpatterns = [
    url(r'^$', EventListCreateView.as_view(), name='event_list_create'),
    url(r'^types/?$', EventTypeListView.as_view(), name='event_type_list'),
]

