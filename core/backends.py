# core/backends.py

from django.contrib.auth.backends import ModelBackend
from .models import SuperAdmin

class SuperAdminAuthenticationBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            superadmin = SuperAdmin.objects.get(email=email)
            if superadmin.check_password(password):
                return superadmin
        except SuperAdmin.DoesNotExist:
            pass
        return None
