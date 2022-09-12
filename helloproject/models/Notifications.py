from django.db import models
from .Teacher import teacher
from .Student import student


class notifications(models.Model):
    sender_email = models.EmailField(max_length=250, default='sender@email.com')
    receiver_email = models.EmailField(max_length=250, default='receiver@email.com')
    is_student_sender = models.BooleanField(max_length=250)
    message = models.CharField(max_length=500)
    timestamp = models.DateTimeField()
