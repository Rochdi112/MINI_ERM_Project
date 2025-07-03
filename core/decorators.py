from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

# Décorateur pour restreindre l'accès selon le rôle utilisateur
def role_required(role):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            profil = getattr(request.user, 'profil_utilisateur', None)
            if profil and profil.role == role:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator
