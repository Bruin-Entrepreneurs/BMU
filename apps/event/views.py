import json
import requests

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from apps.helpers.helpers import get_data_field_or_400, get_data_list_or_400
from apps.event.serializer import EventSerializer, EventTypeSerializer, EventSummarySerializer
from apps.event.models import Event, EventType
from apps.user.models import User


class EventTypeListView(ListAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class EventListCreateView(ListModelMixin, GenericAPIView):
    queryset = Event.objects.filter(end_time__gte=timezone.now())  # Gets all future events
    serializer_class = EventSummarySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        creator = request.user
        users = User.objects.all()

        event_type_id = get_data_field_or_400(request, 'event_type_id')
        start_time = get_data_field_or_400(request, 'start_time')
        end_time = get_data_field_or_400(request, 'end_time')
        super_invite_ids = get_data_list_or_400(request, 'super_invite_ids')
        description = get_data_field_or_400(request, 'description')

        event_type = EventType.objects.get(pk=int(event_type_id))
        event = Event.objects.create(
            creator=creator,
            event_type=event_type,
            start_time=start_time,
            # end_time=end_time,
            description=description
        )

        for super_invite_id in super_invite_ids:
            super_invited_user = User.objects.get(pk=int(super_invite_id))
            event.super_invited.add(super_invited_user)
        event.accepted.add(creator)
        event.save()

        for user in users:
            if user.id in super_invite_ids:
                body = 'You\'ve been SUPER invited by ' + creator.username + '!! YOU BETTER GO HOE'
                sound = 'default'
            else:
                body = 'You\'ve been invited by ' + creator.username + '!'
                sound = None

            requests.post(
                'https://exp.host/--/api/v2/push/send',
                data={
                    "to": user.notification_token,
                    "title": event_type.name + 'at' + str(start_time),
                    "body": body,
                    "data": json.dumps({'id': event.id}),
                    # "sound": sound
                }
            )

        return Response(data=EventSerializer(event).data, status=status.HTTP_201_CREATED)


class EventDetailView(ListModelMixin, RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        event_instance = self.get_queryset().get(pk=self.kwargs['event_id'])
        serializer = self.get_serializer(event_instance)

        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        current_user = request.user
        personal_events = []
        for event in self.get_queryset():
            accepted_users = event.accepted
            for user in accepted_users:
                if user.username = current_user.username:
                    personal_events.append(event)
                    break 
        serializer = self.get_serializer(personal_events, many=True)
        return Response(data=serializer.data)



class EventAcceptView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        event_instance = self.get_queryset().get(pk=self.kwargs['event_id'])

        event_instance.accepted.add(user)
        event_instance.save()
        serializer = self.get_serializer(event_instance)

        return Response(serializer.data)


class EventDeclineView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        event_instance = self.get_queryset().get(pk=self.kwargs['event_id'])

        event_instance.declined.add(user)
        event_instance.save()
        serializer = self.get_serializer(event_instance)

        return Response(serializer.data)
