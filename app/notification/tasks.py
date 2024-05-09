from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task

from waste.models import STSManager, LandfillManager
from .models import UserNotification


@shared_task
def send_notification_to_a_user(user, message):
    notification = UserNotification(user=user, message=message)
    notification.save()


@shared_task
def send_notification_to_group_user(group, message):
    for user in group.users.all():
        send_notification_to_a_user.delay(user, message)


@shared_task
def send_notification_to_sts_manager(sts, message):
    for stsManagers in STSManager.objects.filter(sts=sts).all():
        user = stsManagers.user
        send_notification_to_a_user.delay(user, message)


@shared_task
def send_notification_to_landfill_manager(landfill, message):
    for landfillManager in LandfillManager.objects.filter(landfill=landfill).all():
        user = landfillManager.user
        send_notification_to_a_user.delay(user, message)


@shared_task
def send_notification_task(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": message
        }
    )
