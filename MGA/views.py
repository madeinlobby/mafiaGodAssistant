from django.contrib.auth import login, authenticate, models, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from rest_framework import status, generics, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.response import Response
from rest_framework.reverse import reverse

from MGA.view import UserViews
from . import EmailSender, MakeRandomPassword
from .models import User, Event, Organization
from .permissions import IsOwnerOrAdmin
from .serializers import UserSerializer, EventSerializer, OrganizationSerializer, OrganizationCreateSerializer

# TODO Question
from .view.UserViews import put_user


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username and password:
        user = authenticate(username=username, password=password)
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not user.is_active:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
            # TODO go to another page
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', "GET"])
@login_required
def logout_user(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def signup_user(request):
    try:
        email = request.data.get('email')
        response = UserViews.post_user(request)
        if response == status.HTTP_201_CREATED:
            user = User.objects.get(username=request.data.get('username'))
            login(request, user)
            EmailSender.EmailSender.send_email(email, "Click here to confirm " + user.confirm_url, 'Confirm')
            return Response(status=status.HTTP_200_OK)
        else:
            return response
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def confirm_email(request, id):
    try:
        user = User.objects.get(pk=id)
        user.confirm = True
        user.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET', 'PUT'])
@login_required
@permission_classes([IsOwnerOrAdmin])
def change_password(request):
    oldPassword = request.data.get('oldPassword')
    user = request.user
    if user.check_password(oldPassword):
        user.password = request.data.get('newPassword')
        user.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
    id = request.data.get('id')
    user = User.objects.get(id=id)
    new_password = MakeRandomPassword.MakeRandomPassword.make_pass()
    EmailSender.EmailSender.send_email(user.email,
                                       "Your new Password" + new_password, "Reset Password")

    user.set_password(new_password)
    user.save()
    return Response(status=status.HTTP_200_OK)


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

