from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User


class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


class NotificationBase(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        abstract = True  # This model will not be created in the database


class UserNotification(NotificationBase):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} Notification - {self.timestamp}"
