from django.shortcuts import render, redirect

from .models import UserNotification


# def notification_page_view(request):
#     return render(request, "notification_page.html")

def read_all_notification(request):
    user = request.user
    notifications = UserNotification.objects.filter(
        user=user, read=False).all()
    for notification in notifications:
        notification.read = True
        notification.save()
    return redirect('dashboard')
