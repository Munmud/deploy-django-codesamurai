from .models import UserNotification


def add_notification(user, context):
    context.update({
        "notifications": UserNotification.objects.filter(user=user).order_by('-timestamp').all(),
        "unread_notification_count": UserNotification.objects.filter(user=user, read=False).count()
    })
    return context
