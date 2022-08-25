from django.db import models


class student(models.Model):
    s_name = models.CharField(max_length=200)
    s_id = models.CharField(max_length=50, primary_key=True)
    s_session = models.CharField(max_length=25)
    password = models.CharField(max_length=500)
