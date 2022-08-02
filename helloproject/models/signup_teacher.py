from django.db import models


class signup_teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def reg(self):
        self.save()
    @property
    def get_all_products(self):
        return self.full_name

