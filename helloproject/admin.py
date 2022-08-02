from django.contrib import admin
from .models.product import prod
from .models.category import cate
from .models.signup_teacher import signup_teacher
# Register your models here.
class adminprod(admin.ModelAdmin):
    list_display = ['name','price','category']
class admincate(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(prod,adminprod)
admin.site.register(cate,admincate)
admin.site.register(signup_teacher)
