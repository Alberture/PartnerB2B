from rest_framework import permissions, status

from django.core.exceptions import PermissionDenied

from datetime import datetime

class ConfigureOnlyIfPartner(permissions.BasePermission):
    """
        Permission that ONLY allows a partner to configure a webkooh.
    """
    def has_permission(self, request, view):
        if request.method == 'POST' and request.path == "/api/v1/webhooks/configure/" or request.user.is_staff:
            return True
        
        raise PermissionDenied({
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Permission Error",
                "details":[
                    {
                        "error": "You must be an admin to perform this action.",
                        "action": request.method,
                        "path": request.path
                    }
                ] 
            })

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        raise PermissionDenied({
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Permission Error",
                "details":[
                    {
                        "error": "You must be an admin to perform this action.",
                        "action": request.method,
                        "path": request.path
                    }
                ] 
            })

