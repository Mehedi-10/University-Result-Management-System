from django.contrib import admin
from .models.Teacher import teacher
from .models.Student import student
from .models.Before_Final import before_final
from .models.Courses import courses
from .models.Assigned_Courses import assigned_course
from .models.Final import final
from .models.Improve import improve
from .models.Exam_Committee import exam_committe
from .models.Published import published
from .models.Officially_Published import officially_published
from .models.Notifications import notifications


# Register your models here.
admin.site.register(teacher)
admin.site.register(before_final)
admin.site.register(student)
admin.site.register(courses)
admin.site.register(assigned_course)
admin.site.register(improve)
admin.site.register(final)
admin.site.register(exam_committe)
admin.site.register(published)
admin.site.register(officially_published)
admin.site.register(notifications)
