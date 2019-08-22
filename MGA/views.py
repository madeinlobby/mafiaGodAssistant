from django.contrib.auth import login, authenticate, models, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from rest_framework import status, generics, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.response import Response

from . import EmailSender, MakeRandomPassword
from .models import User, Event, Organization
from .permissions import IsOwnerOrAdmin
from .serializers import PUserSerializer, EventSerializer, OrganizationSerializer, OrganizationCreateSerializer

# TODO Question
from .view.UserViews import put_user

"""
 1.general inja bashe khobe?
 2.signup ro hataman check she
"""


@permission_classes([AllowAny])
def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    if username and password:
        user = authenticate(username=username, password=password)
        if not username:
            return Response(status='Incorrect username')
        if not user.check_password(password):
            return Response(status='Incorrect password')
        if not user.is_active:
            return Response(status='It is not active')
        else:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
            # TODO go to another page
    else:
        return Response(status='Sorry! There is a problem!')


@login_required
def logout_user(request):
    logout(request)
    return Response(status='logout successfully')


def signup_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        serializer = PUserSerializer(request.data)
        if serializer.is_valid:
            serializer.save()
            user = models.User.objects.create(username=username, password=password)
            user.save()
            login(request, user)

            EmailSender.EmailSender.send_email(email, "Click here to confirm " + serializer.confirm_url, 'Confirm')

            return Response(status='Please confirm your Email')
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except:
        return Response(status='Sorry! There is a problem')


def confirm_email(request, id):
    try:
        user = User.objects.get(id=id)
        user.confirm = True
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status='Please confirm your Email')


@permission_classes([IsOwnerOrAdmin])
def change_password(request): #TODO bug dare fekr konam
    newPassword = request.POST['newPassword']
    oldPassword = request.POST['oldPassword']
    id = request.POST['id']
    user = User.objects.get(id=id)
    if user.password == oldPassword:
        return put_user()
    return Response('Your password is Wrong!')


@permission_classes([AllowAny])
def reset_password(request):
    id = request.POST['id']
    user = User.objects.get(id=id)
    new_password = MakeRandomPassword.MakeRandomPassword.make_pass()
    EmailSender.EmailSender.send_email(user.email,
                                       "Your new Password" + new_password, "Reset Password")

    # TODO change password in db
    return Response(status='We send a new password to your email')


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







