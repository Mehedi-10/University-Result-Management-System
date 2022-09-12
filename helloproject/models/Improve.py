from django.db import models
from .Student import student
from .Courses import courses
x=25
class improve(models.Model):
    s_id = models.ForeignKey(student, on_delete=models.CASCADE)
    s_session = models.CharField(max_length=25)
    c_id = models.ForeignKey(courses, on_delete=models.CASCADE)
    r_date=models.DateField()
    total1 = models.CharField(max_length=2 * x, default='0.0')
    total2 = models.CharField(max_length=2 * x, default='0.0')
    totalFinal = models.CharField(max_length=2 * x, default='0.0')
    lattergrade = models.CharField(max_length=5, default='F')
    pointgrade = models.CharField(max_length=x, default='0.0')