from django.contrib.auth import login, authenticate, models, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.response import Response

from . import EmailSender, MakeRandomPassword
from .models import User
from .permissions import IsOwnerOrAdmin
from .serializers import PUserSerializer

# TODO Question
from .view.UserViews import put_user

"""
 1.general inja bashe khobe?
 2.signup ro hataman check she
"""


@permission_classes([AllowAny])
def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        user = authenticate(username=username, password=password)
        if not username:
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


@login_required
def logout_user(request):
    logout(request)
    return Response(status='logout successfully')


def signup_user(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        serializer = PUserSerializer(request.data)
        if serializer.is_valid():
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
