from django.db import models

from MGA.models import User


class Message(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    receiver = models.ManyToManyField(User, related_name="receiver")  # can be a person or a group
