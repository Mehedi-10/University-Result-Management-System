from django.db import models
from .Courses import courses
from .Teacher import teacher
x=25
class published(models.Model):
    c_id=models.ForeignKey(courses,on_delete=models.CASCADE)
    s_session = models.CharField(max_length=x, default='', blank=True)
    t_email = models.ForeignKey(teacher, on_delete=models.CASCADE)
    published_before_final = models.BooleanField(default=False)
    published_final = models.BooleanField(default=False)
    request_edit = models.BooleanField(default=False)
