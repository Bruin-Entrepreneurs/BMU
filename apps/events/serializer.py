from rest_framework import serializers

from apps.events.models import Events

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ( 
            'name',
            'description',
            'type',
            'startTime',
            'endTime', 
            )
