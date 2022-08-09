from django.db import models

class teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=500)
    def reg(self):
        self.save()

