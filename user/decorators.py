from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from functools import wraps

def rol_requerido(nombre_grupo):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.groups.filter(name=nombre_grupo).exists():
                return view_func(request, *args, **kwargs)
            return HttpResponseRedirect('/')  # Redirige a inicio o login
        return _wrapped_view
    return decorator
