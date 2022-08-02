from django.db import models
from .category import cate
class prod(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField(default=0)
    category =models.ForeignKey(cate,on_delete=models.CASCADE,default=1)
    image = models.ImageField(upload_to='products/')
    @staticmethod
    def get_all_products():
        return prod.objects.all()