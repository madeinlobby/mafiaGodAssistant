from django.contrib.auth import login, authenticate, models, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.timezone import now

from rest_framework import status, generics, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.response import Response
from rest_framework.reverse import reverse

from MGA.view import UserViews
from MGA.models import User, Event, Organization, Friend, Notification
from MGA.permissions import IsOwnerOrAdmin
from MGA.serializers import UserSerializer, EventSerializer, OrganizationSerializer, OrganizationCreateSerializer, \
    NotificationSerializer

from .UserViews import put_user


@api_view(['GET'])
def event_details(request, pk):
    if request.method == 'GET':
        event = Event.objects.all().get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(['GET', 'PUT', 'POST'])
# def event_list(request):
#     if request.method == 'GET':
#         events = Event.objects.all()
#         serializer = EventSerializer(events, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(status=status.HTTP_404_NOT_FOUND)

# todo this v or that ^?


class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# @api_view(['GET', 'PUT', 'POST'])
# def organization_list(request):
#     if request.method == 'GET':
#         organizations = Organization.objects.all()
#         serializer = OrganizationSerializer(organizations, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         serializer = OrganizationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(status=status.HTTP_404_NOT_FOUND)


class OrganizationList(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrganizationCreateSerializer
        return OrganizationSerializer

