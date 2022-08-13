from django.db import models


class courses(models.Model):
    course_name = models.CharField(max_length=200)
    course_id = models.CharField(max_length=100)
    syllabus_year = models.CharField(max_length=200)
    credit = models.IntegerField()
