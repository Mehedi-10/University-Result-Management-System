from django.db import models
from .Courses import courses
x=25
class final(models.Model):
    c_id=models.ForeignKey(courses,on_delete=models.CASCADE)
    s_session=models.CharField(max_length=x,default='',blank=True)
    s_id=models.CharField(max_length=100,default='',blank=True)
    total1=models.CharField(max_length=2*x,default='',blank=True)
    total2=models.CharField(max_length=2*x,default='',blank=True)
    totalFinal=models.CharField(max_length=2*x,default='',blank=True)
    lattergrade=models.CharField(max_length=5,default='',blank=True)
    pointgrade=models.CharField(max_length=x,default='',blank=True)