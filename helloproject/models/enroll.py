from django.db import models

class enroll(models.Model):
    course_id = models.CharField(max_length=1000)
    sid= models.CharField(max_length=50)