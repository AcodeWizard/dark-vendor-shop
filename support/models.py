from datetime import datetime
from uuid import uuid4
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    name = models.ForeignKey(User, related_name='name', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    started = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField(null=True, blank=True)


class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, related_name='chat', on_delete=models.CASCADE)
    name = models.ForeignKey(User, related_name='chat_message_name', on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    message = models.TextField()
    sent = models.DateTimeField(auto_now_add=True)

class Ticket(models.Model):
    sub_title = models.CharField(max_length=200)
    sub_description = models.TextField()
    name = models.ForeignKey(User, related_name='ticket', on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sub_title

class Ticket_replay(models.Model):
    sub_description = models.TextField()
    ticket = models.ForeignKey(Ticket, related_name='title', on_delete=models.CASCADE)
    admin = models.BooleanField(default=False)
    sent = models.DateTimeField(auto_now_add=True)