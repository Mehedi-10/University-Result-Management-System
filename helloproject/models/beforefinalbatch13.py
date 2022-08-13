from django.db import models


class before_final_table(models.Model):
    CourseidandTeacherid=models.CharField(max_length=1000,default="")
    Student_id=models.CharField(max_length=100,null=True,blank=True)
    A = models.CharField(max_length=100,null=True,blank=True)
    B = models.CharField(max_length=100,null=True,blank=True)
    C = models.CharField(max_length=100,null=True,blank=True)
    D = models.CharField(max_length=100,null=True,blank=True)
    E = models.CharField(max_length=100,null=True,blank=True)
    F = models.CharField(max_length=100,null=True,blank=True)
    G = models.CharField(max_length=100,null=True,blank=True)
    H = models.CharField(max_length=100,null=True,blank=True)
    I = models.CharField(max_length=100,null=True,blank=True)
