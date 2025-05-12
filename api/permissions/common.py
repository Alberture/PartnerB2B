from rest_framework import permissions, status

from django.core.exceptions import PermissionDenied

from datetime import datetime


class IsAdminToDeletePutPatch(permissions.BasePermission):
    """
        Permission that ONLY allow the admin to DELETE, PUT or PATCH
    """
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if not request.user.is_staff:
                raise PermissionDenied({
                    "error":{
                        "code": status.HTTP_403_FORBIDDEN,
                        "message": "Permission Error",
                        "details":[
                            {"error": "You must be an admin to perform this action."}
                        ]
                    },
                    "meta":{
                        "timestamp": datetime.now()
                    }
                })
            
        return True