from ninja.errors import HttpError
from functools import wraps

def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            # Cek field 'role' sesuai User model kamu
            if request.user.role not in roles and not request.user.is_superuser:
                raise HttpError(403, f"Akses ditolak. Role {roles} diperlukan.")
            return func(request, *args, **kwargs)
        return wrapper
    return decorator