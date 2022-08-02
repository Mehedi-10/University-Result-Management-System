from django.db import models
from .signup_teacher import signup_teacher
class login_teacher(models.Model):
    all=signup_teacher.get_all_products
    print(all)


