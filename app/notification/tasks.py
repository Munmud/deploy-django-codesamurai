# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
from celery import shared_task
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from waste.models import STSManager, LandfillManager, Landfill, STS
from .models import UserNotification


@shared_task
def send_notification_to_a_user(username, title, message):
    user = User.objects.get(username=username)
    notification = UserNotification(user=user, title=title, message=message)
    notification.save()


@shared_task
def send_notification_to_group_user(group_id, title, message):
    group = Group.objects.get(id=group_id)
    for user in group.users.all():
        send_notification_to_a_user.delay(user.username, title, message)


@shared_task
def send_notification_to_sts_manager(sts_id, title, message):
    sts = STS.objects.get(id=sts_id)
    for stsManagers in STSManager.objects.filter(sts=sts).all():
        user = stsManagers.user
        send_notification_to_a_user.delay(user.username, title, message)


@shared_task
def send_notification_to_landfill_manager(landfill_id, title, message):
    landfill = Landfill.objects.get(id=landfill_id)
    for landfillManager in LandfillManager.objects.filter(landfill=landfill).all():
        user = landfillManager.user
        send_notification_to_a_user.delay(user.username, title, message)


# @shared_task
# def send_notification_task(message):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "notifications",
#         {
#             "type": "send_notification",
#             "message": message
#         }
#     )
