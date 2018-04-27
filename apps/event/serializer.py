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
    super_invited = serializers.SerializerMethodField()

    def get_super_invited(self, obj):
        data = []

        for user in obj.super_invited.all():
            data.append(UserSummarySerializer(user).data)

        return data


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
