from django.db import models
import uuid
import datetime


class teacher(models.Model):
    t_name = models.CharField(max_length=200)
    t_email = models.EmailField(max_length=254, primary_key=True)
    password = models.CharField(max_length=500)
    code = models.CharField(max_length=25, default=uuid.uuid4().hex[:8])
    # code_time=models.DateTimeField()
