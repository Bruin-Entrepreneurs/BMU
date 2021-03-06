from rest_framework import serializers

from apps.event.models import Event, EventType
from apps.user.serializer import UserSummarySerializer


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'id',
            'name',
            'image_url'
        )


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'creator',
            'event_type',
            'accepted',
            'declined',
            'super_invited',
            'description',
            'start_time',
            'end_time',
        )

    event_type = EventTypeSerializer()
    accepted = UserSummarySerializer(many=True)
    declined = UserSummarySerializer(many=True)


class EventSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'event_type',
            'accepted',
            'super_invited',
            'start_time',
        )

    event_type = EventTypeSerializer()
