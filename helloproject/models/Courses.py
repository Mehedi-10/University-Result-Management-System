from django.db import models


class courses(models.Model):
    c_name = models.CharField(max_length=200)
    c_id=models.CharField(max_length=200,primary_key=True)
    credit=models.FloatField()
