from django.db import models

class teaches(models.Model):
    course_id = models.CharField(max_length=1000)
    T_email = models.CharField(max_length=500)