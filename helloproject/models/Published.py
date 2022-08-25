from django.db import models
from .Courses import courses
x=25
class published(models.Model):
    c_id=models.ForeignKey(courses,on_delete=models.CASCADE)
    s_session=models.CharField(max_length=x,default='',blank=True)
    published_before_final=models.BooleanField(default=False)
    published_final=models.BooleanField(default=False)
