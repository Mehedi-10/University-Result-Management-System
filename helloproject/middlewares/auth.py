from django.shortcuts import redirect
def is_allowed(get_response):
    # One-time configuration and initialization.

    def gaurd(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('hello')
        if not request.session.get('email'):
            return redirect('index_page')
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return gaurd
def is_allowed_student(get_response):
    # One-time configuration and initialization.

    def gaurd(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        print('hello')
        if not request.session.get('sid'):
            return redirect('index_page')
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return gaurd