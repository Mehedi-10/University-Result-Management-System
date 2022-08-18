from django.db import models

class table(models.Model):
    Ecourseid = models.CharField(max_length=1000)
    size=models.IntegerField(default=3)