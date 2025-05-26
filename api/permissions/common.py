from rest_framework import permissions, status
from rest_framework.exceptions import MethodNotAllowed
from ..models import Partner

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
    
class ListAndRetrieveOnly(permissions.BasePermission):
    """
        Permission that allows retrieve and list action ONLY.
    """
    def has_permission(self, request, view):
        if view.action == 'retrieve' or view.action == 'list':
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
    
class UpdateNotAllowed(permissions.BasePermission):
    """
        Permission that does not allow update and list actions.
    """
    def has_permission(self, request, view):
        if request.method != 'PUT':
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

class IsAdminOrPartnerActivationStatusIsSuccessOrNotAllowed(permissions.BasePermission):
    """
        Permission allows only partner with activation status as success
        to manage their profiles.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True

        partner = Partner.get_authenticated_partner(request)
        if not partner.activationStatus == "success":
            raise MethodNotAllowed({
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Not Allowed",
                "details":[
                    {
                        "error": "Your api key is not activated yet."
                    }
                ]
            })

        return True