from django.db import models
from django.contrib.auth.models import User


class Sample(models.Model):
    attachment = models.FileField()


# class IssueReport(models.Model):
#     REPORT_CHOICES = [
#         ('Overflowing', 'Overflowing'),
#         ('Damaged', 'Damaged'),
#         ('Missing', 'Missing'),
#         ('Other', 'Other'),
#     ]
#     reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     report_type = models.CharField(max_length=20, choices=REPORT_CHOICES)
#     description = models.TextField()
#     reported_at = models.DateTimeField(auto_now_add=True)
#     resolved = models.BooleanField(default=False)


# class ForumPost(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


# class ForumComment(models.Model):
#     post = models.ForeignKey(
#         ForumPost, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)


# class Event(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField()
#     location = models.CharField(max_length=200)
#     date = models.DateTimeField()
#     organizer = models.ForeignKey(User, on_delete=models.CASCADE)
#     participants = models.ManyToManyField(
#         User, related_name='events_participated', blank=True)

#     def __str__(self):
#         return self.name


# class Volunteer(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     registration_link = models.URLField()


# # class Language(models.Model):
# #     name = models.CharField(max_length=100)


# # class PrivacySettings(models.Model):
# #     user = models.OneToOneField(
# #         User, on_delete=models.CASCADE, related_name='privacy_settings')
# #     hide_profile = models.BooleanField(default=False)
# #     hide_activity = models.BooleanField(default=False)
