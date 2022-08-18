from django.contrib import admin
from .models.teacher import teacher
from .models.student import student
from .models.beforefinalbatch13 import before_final_table
from .models.courses import courses
from .models.enroll import enroll
from .models.teaches import teaches

# Register your models here.
admin.site.register(teacher)
admin.site.register(before_final_table)
admin.site.register(student)
admin.site.register(courses)
admin.site.register(enroll)
admin.site.register(teaches)

