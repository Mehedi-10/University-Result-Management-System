from django.shortcuts import redirect
from helloproject.models import Student,Teacher
from django.contrib import messages
def is_allowed(get_response):
    def gaurd(request):

        if not request.session.get('email') or not Teacher.teacher.objects.filter(t_email=request.session.get('email')).exists():
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

        if not request.session.get('email') or not Student.student.objects.filter(s_id=request.session.get('email')).exists():
            # messages.warning(request,'Sign in first')
            return redirect('who_are_you')
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return student_gaurd


def is_allowed_to_change_pass(get_response):
    def checkuser(request):
        if not request.session.get('to_verify'):
            return redirect('who_are_you')
        response = get_response(request)
        return response

    return checkuser


def is_admin(get_response):
    def checkadmin(request):
        if not request.session.get('email'):
            return redirect('who_are_you')
        response = get_response(request)
        return response

    return checkadmin
