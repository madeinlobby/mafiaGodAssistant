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

from MGA import GeneralFunctions
from MGA.view import UserViews
from . import EmailSender, MakeRandomPassword
from .models import User, Event, Organization, Friend, Notification, Reason, Report
from .permissions import IsOwnerOrAdmin
from .serializers import UserSerializer, EventSerializer, OrganizationSerializer, OrganizationCreateSerializer, \
    NotificationSerializer, ReasonSerializer

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


@api_view(['POST', 'GET'])
@login_required
def send_friendship_request(request):
    try:
        id = request.data.get('id')
        user = User.objects.get(id=id)
        notification = Notification.objects.create(to_user=User.objects.get(id=request.user.id), text="Friendship",
                                                   time=now(), from_user=request.user)
        notification.save()
        # user.notification_set.add(notification)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
def accept_friendship_request(request):
    try:
        id = request.data.get('id')
        user = User.objects.get(id=id)
        friend = Friend.objects.create()
        friend.friends.add(user)
        friend.friends.add(request.user)
        friend.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def get_all_notifications(request):
    id = request.data.get('id')
    user = User.objects.get(id=id)
    notifications = Notification.objects.get(to_user=user)
    notificationSerializer = NotificationSerializer(notifications, many=True)
    return Response(notificationSerializer.data)


def get_not_read_notification(request):
    id = request.data.get('id')
    user = User.objects.get(id=id)
    notifications = Notification.objects.get(to_user=user, read=False)
    notificationSerializer = NotificationSerializer(notifications, many=True)
    return Response(notificationSerializer.data)


def get_reasons(request):
    reasons = Reason.objects.all()
    serializer = ReasonSerializer(reasons, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def create_report(request):
    reason_pk = request.data.get('reason_pk')
    user_id = request.data.get('user_id')
    reason = Reason.objects.get(pk=reason_pk)
    user = User.objects.get(id=user_id)
    report = Report.objects.create(user=user, r_reason=reason)
    report.save()


def send_report(request):
    report_id = request.data.get('report_id')
    report = Report.objects.get(id=report_id)
    reported_user = report.user
    reasons = report.r_reason
    reason_string = GeneralFunctions.make_reported_string(reasons)

    notification = Notification.objects.create(from_user=request.user, to_user=reported_user
                                               , text="Reporting!!!" +
                                                      " Reason(s):" + reason_string,
                                               time=now())
    notification.save()
