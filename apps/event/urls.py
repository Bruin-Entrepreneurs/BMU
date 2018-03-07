from django.conf.urls import url
from apps.event.views import EventListCreateView

urlpatterns = [
    url(r'^$', EventListCreateView.as_view(), name='event_create')
]

