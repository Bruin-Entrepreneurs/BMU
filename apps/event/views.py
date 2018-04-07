from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework import status

from apps.helpers.helpers import get_data_field_or_400, get_data_list_or_400
from apps.event.serializer import EventSerializer, EventTypeSerializer
from apps.event.models import Event, EventType
from apps.helpers.permissions import IsUser
from apps.user.models import User


class EventTypeListView(ListAPIView):
    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer


class EventListCreateView(ListModelMixin, GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsUser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        event_type_id = get_data_field_or_400(request, 'event_type_id')
        start_time = get_data_field_or_400(request, 'start_time')
        end_time = get_data_field_or_400(request, 'end_time')
        super_invite_ids = get_data_list_or_400(request, 'super_invite_ids')
        description = get_data_field_or_400(request, 'description')

        event = Event.objects.create(
            creator=request.user,
            event_type=EventType.objects.get(pk=event_type_id),
            # start_time=start_time,
            # end_time=end_time,
            description=description
        )

        for super_invite_id in super_invite_ids:
            event.super_invited.add(User.objects.get(pk=super_invite_id))
        event.accepted.add(request.user)
        event.save()

        return Response(data=EventSerializer(event).data, status=status.HTTP_201_CREATED)
