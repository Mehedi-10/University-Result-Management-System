from django.db import models


class marks_1s(models.Model):
    marks=[0]*10
    for i in marks:
        i=models.IntegerField(default=0)
