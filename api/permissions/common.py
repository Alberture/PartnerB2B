from rest_framework import permissions, status
from rest_framework.exceptions import MethodNotAllowed

class RetrieveOnly(permissions.BasePermission):
    """
        Permission that allows retrieve action ONLY.
    """
    def has_permission(self, request, view):
        if view.action == 'retrieve':
            return True

        raise MethodNotAllowed({
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Not Allowed",
                "details":[
                    {
                        "error": "Method \"%s\" not allowed." % (request.method),
                        "path": request.path
                    }
                ]
            },
        )
    
class UpdateAndListNotAllowed(permissions.BasePermission):
    """
        Permission that does not allow update and list actions.
    """
    def has_permission(self, request, view):
        if view.action != 'list' and request.method != 'PUT':
            return True
        
        raise MethodNotAllowed({
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Not Allowed",
                "details":[
                    {
                        "error": "Method \"%s\" not allowed." % (request.method),
                        "path": request.path
                    }
                ]
            },
        )
    
class CantListUpdateCreate(permissions.BasePermission):
    """
        Permission that does not allow list update and create actions.
    """
    def has_permission(self, request, view):
        if view.action not in ['list', 'create'] and request.method != 'PUT':
            return True
        
        raise MethodNotAllowed({
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Not Allowed",
                "details":[
                    {
                        "error": "Method \"%s\" not allowed." % (request.method),
                        "path": request.path
                    }
                ]
            },
        )