from django.shortcuts import redirect
from helloproject.models import student,teacher
from django.contrib import messages
def is_allowed(get_response):
    def gaurd(request):

        if not request.session.get('email') or not teacher.teacher.objects.filter(email=request.session.get('email')).exists():
            # messages.warning(request,'Sign in first')
            return redirect('who_are_you')
        response = get_response(request)

        return response

    return gaurd

def is_allowed_student(get_response):
    # One-time configuration and initialization.

    def student_gaurd(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.session.get('email') or not student.student.objects.filter(sid=request.session.get('email')).exists():
            # messages.warning(request,'Sign in first')
            return redirect('who_are_you')
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return student_gaurd