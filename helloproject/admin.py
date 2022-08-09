from django.contrib import admin
from .models.teacher import teacher
from .models.student import student
from .models.beforefinalbatch13 import marks_1s
# Register your models here.
class adminprod(admin.ModelAdmin):
    list_display = ['name','price','category']
class admincate(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(teacher)
admin.site.register(marks_1s)
admin.site.register(student)

