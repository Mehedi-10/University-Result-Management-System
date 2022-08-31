from django.db import models
from .Courses import courses
from .Teacher import teacher
from .Student import student


class assigned_course(models.Model):
    c_id = models.ForeignKey(courses, on_delete=models.CASCADE)
    t_mail = models.ForeignKey(teacher, on_delete=models.CASCADE)
    s_session = models.CharField(max_length=50, default='')
    # guest = internal/external/
    guest = models.CharField(max_length=50, default='')
