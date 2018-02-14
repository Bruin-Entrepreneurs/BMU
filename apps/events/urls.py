from django.conf.urls import url
from apps.events import views

urlpatterns = [
    url(r'^eventSet', views.get_all_events_or_post, name='get_or_post')
]

