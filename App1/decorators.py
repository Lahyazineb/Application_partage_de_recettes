from django.http import HttpResponse
from django.shortcuts import redirect,render

def user_not_authenticated(function=None, redirect_url='/'):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request, 'user') and request.user.is_authenticated:
                return redirect(redirect_url)
            else:
                return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request , *args , **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request , *args , **kwargs)
            else:
                return render(request, 'app1/NotAllowed.html',)
        return wrapper_func
    return decorator
