from django.db import models
from .Teacher import teacher
from .Student import student


class chats(models.Model):
    s_id = models.ForeignKey(student, on_delete=models.CASCADE)
    t_id = models.ForeignKey(teacher, on_delete=models.CASCADE)
    is_student_sender = models.BooleanField()
    message = models.CharField(max_length=500)
    timestamp = models.DateTimeField()
