from django.db import models
from .Teacher import teacher

class exam_committe(models.Model):
    t_mail1=models.ForeignKey(teacher,related_name='Chairman',on_delete=models.CASCADE)
    t_mail2=models.ForeignKey(teacher,related_name='Member1',on_delete=models.CASCADE)
    t_mail3=models.ForeignKey(teacher,related_name='Member2',on_delete=models.CASCADE)