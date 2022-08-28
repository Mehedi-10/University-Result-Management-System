from django.db import models
import uuid
import datetime


class student(models.Model):
    s_name = models.CharField(max_length=200)
    s_id = models.CharField(max_length=50, primary_key=True)
    s_session = models.CharField(max_length=25)
    password = models.CharField(max_length=500)
    s_email = models.EmailField(max_length=254, default='abc@gmail.com')
    code = models.CharField(max_length=25, default=uuid.uuid4().hex[:8])
    # code_time=models.DateTimeField()
