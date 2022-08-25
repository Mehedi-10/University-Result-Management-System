from django.db import models
from .Courses import courses
from .Student import student
x=50
class before_final(models.Model):
    c_id=models.ForeignKey(courses,on_delete=models.CASCADE)
    s_session=models.CharField(max_length=x,default='',blank=True)
    s_id=models.CharField(max_length=100,default='',blank=True)
    mid1=models.CharField(max_length=x,default='',blank=True)
    mid2=models.CharField(max_length=x,default='',blank=True)
    mid3=models.CharField(max_length=x,default='',blank=True)
    class_test=models.CharField(max_length=x,default='',blank=True)
    presentation=models.CharField(max_length=x,default='',blank=True)
    attendance=models.CharField(max_length=x,default='',blank=True)
    assignment=models.CharField(max_length=x,default='',blank=True)
    extra_field=models.CharField(max_length=x,default='',blank=True)
    total=models.CharField(max_length=x,default='',blank=True)
    total_ump = models.CharField(max_length=x, default='', blank=True)