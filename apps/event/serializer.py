from rest_framework import serializers

from apps.event.models import Event, EventType


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'name',
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'creator',
            'activity_type',
            'accepted',
            'super_invited',
            'description',
            'start_time',
            'end_time',
        )


class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'activity_type',
            'accepted',
            'super_invited',
            'start_time',
        )