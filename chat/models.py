from django.db import models

from MGA.models import User


class Message(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    receiver = models.ManyToManyField(User, related_name="receiver")  # can be a person or a group


class Group(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_owner')
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(User, related_name='group_members')


class Reply(Message):
    message = models.ForeignKey(Message, on_delete=models.CASCADE,related_name='message_reply')
