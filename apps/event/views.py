import requests
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status

from apps.helpers.helpers import get_data_field_or_400, get_data_list_or_400
from apps.event.serializer import EventSerializer, EventTypeSerializer, EventSummarySerializer
from apps.event.models import Event, EventType
from apps.user.models import User


class EventTypeListView(ListAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class EventListCreateView(ListModelMixin, GenericAPIView):
    queryset = Event.objects.all()
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
            # start_time=start_time,
            # end_time=end_time,
            description=description
        )

        for super_invite_id in super_invite_ids:
            super_invited_user = User.objects.get(pk=int(super_invite_id))
            event.super_invited.add(super_invited_user)
        event.accepted.add(creator)
        event.save()

        for user in users:
            requests.post(
                'https://exp.host/--/api/v2/push/send',
                data={
                    "to": user.notification_token,
                    "title": event_type.name,
                    "body": 'You\'ve been invited by ' + '!'
                }
            )

        return Response(data=EventSerializer(event).data, status=status.HTTP_201_CREATED)


class EventDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get(self, request, *args, **kwargs):
        event_instance = self.get_queryset().get(pk=self.kwargs['event_id'])
        serializer = self.get_serializer(event_instance)

        return Response(serializer.data)


class EventAcceptView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        event_instance = self.get_queryset().get(pk=self.kwargs['event_id'])

        event_instance.accept.add(user)
        event_instance.save()
        serializer = self.get_serializer(event_instance)

        return Response(serializer.data)


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