from django.utils.timezone import now

from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from MGA.models import User, Event, Organization, AdminShip, MemberShip
from MGA.serializers import EventSerializer, OrganizationSerializer, OrganizationCreateSerializer


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


@api_view(['GET', 'POST'])
def add_organization(request):
    try:
        organization = Organization.objects.create(name=request.data.get('name'),
                                                   creator=request.user,
                                                   )
        serializer = OrganizationSerializer(organization)
        organization.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_admins(request):
    admin_id = request.data.get('admin id')
    organization_id = request.data.get('org_id')
    organization = Organization.objects.get(id=organization_id)
    if request.user != organization.creator:
        return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        user = User.objects.get(id=admin_id)
        adminship = AdminShip(admin=user, organization=organization)
        adminship.save()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def add_event(request):
    organization_id = request.data.get('org_id')
    organization = Organization.objects.get(id=organization_id)
    if request.user == organization.creator or request.user in organization.admins.all():
        qs = Event.objects.filter(title__exact=request.data.get('title'))
        if qs.exists():
            return ValidationError('Title should be unique')
        event = Event.objects.create(title=request.data.get('title'),
                                     description=request.data.get('description'),
                                     owner=request.user,
                                     capacity=request.data.get('capacity'),
                                     date=request.data.get('date'),
                                     organization=organization
                                     )
        event.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_403_FORBIDDEN)


def end_event(request):
    return


@api_view(['POST', 'GET'])
def join_event(request, event_id):
    user = request.user
    event = Event.objects.get(id=event_id)
    organization = event.organization
    if user in organization.ban_set.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    membership = MemberShip(event=event, member=user)
    membership.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_public_events(request):
    events = Event.objects.filter(private=False)
    serializer = EventSerializer(events)
    return Response(serializer.data)


"""
 in search item you should pass number
 
"""


# TODO add search by cafe and location


@api_view(['GET'])
def search_event(request):
    try:
        search_item = request.data.get('search_item')
        if search_item == 1:
            events = Event.objects.filter(private=False)
        elif search_item == 2:
            events = Event.objects.filter(private=True)
        elif search_item == 3:
            events = Event.objects.filter(date__day=now().day)
        elif search_item == 4:
            events = Event.objects.filter(date__month=now().month)

        serializer = EventSerializer(events)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])  # for test do not use
def add_member(request):
    user_id = request.data.get('user_id')
    user = User.objects.get(id=user_id)
    event_id = request.data.get('event_id')
    event = Event.objects.get(id=event_id)
    membership = MemberShip.objects.create(event=event, member=user)
    membership.save()
    user.save()
    return Response(status=status.HTTP_200_OK)
