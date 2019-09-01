from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from pushy.utils import send_push_notification
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from MGA.models import User
from chat.models import Message, Group, Reply
from chat.permissions import IsOwner
from chat.serializers import MessageSerializer, GroupSerializer, ReplySerializer


@login_required
@api_view(['POST'])
def send_to_one(request):
    try:
        receiver_id = request.data.get('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        message = Message.objects.create(text=request.data.get('text'), owner=request.user,
                                         time=now())
        message.receiver.add(receiver)
        message.save()
        # send_push_notification('YOUR_TITLE', MessageSerializer(message).data,  #TODO uncomment
        #                        device=receiver.user_device, store=False)

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def send_to_group(request):
    try:
        group_id = request.data.get('group_id')
        group = Group.objects.get(id=group_id)
        message = Message.objects.create(text=request.data.get('text'), owner=request.user,
                                         time=now())
        for member in group.members.all():
            message.receiver.add(member)
            send_push_notification('YOUR_TITLE', MessageSerializer(message).data,
                                   device=member.user_device, store=False)
        message.save()

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def create_group(request):
    try:
        name = request.data.get('name')
        group = Group.objects.create(name=name, owner=request.user)
        group.save()
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
def create_reply(request):
    try:
        message_id = request.data.get('message_id')
        message = Message.objects.get(id=message_id)
        receiver_id = request.data.get('receiver_id')
        receiver = User.objects.get(id=receiver_id)
        reply = Reply.objects.create(text=request.data.get('text'), owner=request.user,
                                     time=now(), message=message)
        reply.receiver.add(receiver)
        reply.save()
        send_push_notification('YOUR_TITLE', MessageSerializer(reply).data,
                               device=receiver.user_device, store=False)

        serializer = ReplySerializer(reply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsOwner])
def edit_message(request):
    try:
        message_id = request.data.get('message_id')
        message = Message.objects.get(id=message_id)
        new_text = request.data.get('new_text')
        message.text = new_text
        message.save()
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'PUT', 'PATCH'])
@permission_classes([IsOwner])
def edit_Reply(request):
    try:
        reply_id = request.data.get('reply_id')
        reply = Reply.objects.get(id=reply_id)
        new_text = request.data.get('new_text')
        reply.text = new_text
        reply.save()
        serializer = ReplySerializer(reply)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)


class RetrieveMessageView(generics.RetrieveAPIView):
    queryset = Message
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class DestroyUpdateMessageView(generics.DestroyAPIView, mixins.UpdateModelMixin):
    queryset = Message
    serializer_class = MessageSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'


class RetrieveGroupView(generics.RetrieveAPIView):
    queryset = Group
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class DestroyUpdateGroupView(generics.DestroyAPIView, mixins.UpdateModelMixin):
    queryset = Group
    serializer_class = GroupSerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'


class RetrieveReplyView(generics.RetrieveAPIView):
    queryset = Reply
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class DestroyUpdateReplyView(generics.DestroyAPIView, mixins.UpdateModelMixin):
    queryset = Reply
    serializer_class = ReplySerializer
    permission_classes = [IsOwner]
    lookup_field = 'id'
