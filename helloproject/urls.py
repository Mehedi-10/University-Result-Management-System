from django.urls import path
from .views import *
urlpatterns = [
    path('', index,name='index_page'),
    path('teacherlogin.html', signin_T),
    path('register_user.html',signup),
    path('teacherresult.html',selectresult),
    path('teacher_beforeFinal.html',fun),
    path('nothing', saving),
    path('excel.html',excelup),
]
