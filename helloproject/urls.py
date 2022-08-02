from django.urls import path
from .views import *
urlpatterns = [
    path('', index),
    path('teacherlogin.html', signin_T),
    path('register_user.html',signup),
]
