from django.db import models

class teacher(models.Model):
    t_name = models.CharField(max_length=200)
    t_email=models.EmailField(max_length = 254,primary_key=True)
    password=models.CharField(max_length=500)
