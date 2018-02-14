from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from .serializer import EventsSerializer
from .models import Events
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'POST'])
def get_all_events_or_post(request):
    if request.method == 'GET':
        events = Events.objects.all()
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data)
    else:
        #need to add in date and time fields for this
        eventData = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            }
        serializer = EventsSerializer(data=eventData)
        if serializer.isValid():
            serializer.save()
            #need to change this to maybe a 200, which the front end can interpret as success
            return Response(serializer.data)
        #need some 404 error couldn't post the data
