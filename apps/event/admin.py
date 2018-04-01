from django.contrib import admin

from apps.event.models import EventType, Event


class EventTypeAdmin(admin.ModelAdmin):
    model = EventType


class EventAdmin(admin.ModelAdmin):
    model = Event


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
