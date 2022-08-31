from django.db import models

class officially_published(models.Model):
    s_session=models.CharField(max_length=25,default='',blank=True)
    # 4-4 format
    s_semester=models.CharField(max_length=200,default='',blank=True)
    is_published=models.BooleanField()