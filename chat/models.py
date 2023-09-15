from django.db import models
from django.contrib.auth import get_user_model
from notify.models import Notification
from django.db.models.signals import post_save
import requests

User = get_user_model()


class Room(models.Model):
    title = models.CharField(max_length=200, null=True,
                             blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    firstuser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="firstuser")
    seconduser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="seconduser")
    joinUser = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


def room_action(sender, **kwargs):
    if kwargs['created']:
        room = kwargs['instance']
        content = f'채팅방을 생성하셨습니다.'
        noti = Notification.objects.create(
            sender=room.firstuser, receiver=room.seconduser, content=content)


post_save.connect(room_action, sender=Room)


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False, null=True, blank=True)
    content = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


def message_action(sender, **kwargs):
    if kwargs['created']:
        message = kwargs['instance']
        room = message.room

        if room.firstuser == message.writer:
            receiver = room.seconduser
        else:
            receiver = room.firstuser

        content = f'메시지를 보내셨습니다.'
        if not message.is_read:
            noti = Notification.objects.create(
                sender=message.writer, receiver=receiver, content=content)
            datas = {
                'notify_id': noti.id
            }
            url = "http://127.0.0.1:8000/notify/massage/"
            res = requests.post(url, data=datas)


post_save.connect(message_action, sender=Message)
