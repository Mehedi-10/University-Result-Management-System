from django.db import models

class student(models.Model):
    full_name = models.CharField(max_length=100)
    sid = models.CharField(max_length=20)
    password = models.CharField(max_length=500)
    s_session = models.CharField(max_length=50)



