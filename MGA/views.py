from django.contrib.auth import login, authenticate, models, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
# from pushy.models import Device
# from pushy.utils import send_push_notification

from rest_framework import status, generics, viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from MGA import GeneralFunctions
from MGA.view import UserViews
from . import EmailSender, MakeRandomPassword
from .models import User, Event, Organization, Friend, Notification, Reason, Report, Ban
from .permissions import IsOwnerOrAdmin
from .serializers import NotificationSerializer, ReasonSerializer


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
            # if request.data.get('device') == 'android':
            # user.user_device = Device.objects.create(key=user.id, type=Device.DEVICE_TYPE_ANDROID, user=user)
            # elif request.data.get('device') == 'ios':
            # Device.objects.create(key=user.id, type=Device.DEVICE_TYPE_IOS, user=user)
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
        notification = Notification.objects.create(to_user=user, text="Friendship",
                                                   time=now(), from_user=request.user)
        notification.save()
        # send_push_notification('YOUR_TITLE', NotificationSerializer(notification).data,
        #                        device=notification.to_user.user_device, store=False)
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
        friend.user = request.user
        friend.friend = user
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
    # send_push_notification('YOUR_TITLE', NotificationSerializer(notification).data, device=notification.to_user.user_device,
    #                        store=False)


def create_ban(request):
    banned_user_id = request.data.get('banned_id')
    organization_id = request.data.get('organization_id')
    reason_id = request.data.get('reason_id')
    organization = Organization.objects.get(id=organization_id)
    banned_user = User.objects.get(id=banned_user_id)
    ban = Ban.objects.create(reason_id=reason_id, user=banned_user, organization=organization)
    ban.save()
    return Response(status=status.HTTP_200_OK)


def send_ban(request):
    ban_id = request.data.get('ban_id')
    ban = Ban.objects.get(id=ban_id)
    banned_user = ban.user
    banned_reason = GeneralFunctions.make_reported_string(ban.b_reason)
    notification = Notification.objects.create(to_user=banned_user, from_user=request.user,
                                               time=now(), text="Ban!!!" +
                                                                "Reason(s)" + banned_reason)
    notification.save()
    # send_push_notification('YOUR_TITLE', NotificationSerializer(notification).data, device=notification.to_user.user_device, store=False)
    return Response(status=status.HTTP_200_OK)


def objection(request):
    try:
        ban_id = request.data.get('ban_id')
        ban = Ban.objects.get(id=ban_id)
        admins = ban.organization.admins.all()
        for admin in admins:
            notification = Notification.objects.create(to_user=admin, from_user=request.user, text="Ban Objection",
                                                       time=now())
            notification.save()
            # send_push_notification('YOUR_TITLE', NotificationSerializer(notification).data,
            #                        device=notification.to_user.user_device, store=False)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
