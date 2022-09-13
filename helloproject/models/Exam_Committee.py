from django.db import models
from .Teacher import teacher

class exam_committe(models.Model):
    t_email1 = models.ForeignKey(teacher, related_name='Chairman', on_delete=models.CASCADE)
    t_email2 = models.ForeignKey(teacher, related_name='Member1', on_delete=models.CASCADE)
    t_email3 = models.ForeignKey(teacher, related_name='Member2', on_delete=models.CASCADE)
    ec_status = models.BooleanField(default=False)
    s_session = models.CharField(max_length=250, default='', blank=True)
