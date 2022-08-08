from django.contrib import admin
from .models.signup_teacher import signup_teacher
from .models.beforefinalbatch13 import marks_1s
# Register your models here.
class adminprod(admin.ModelAdmin):
    list_display = ['name','price','category']
class admincate(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(signup_teacher)
admin.site.register(marks_1s)
