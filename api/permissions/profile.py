from rest_framework import permissions, status

from ..models import Profile, Analysis, ProfileAttributeDocument, Partner

from django.core.exceptions import PermissionDenied

from datetime import datetime

class ProfileBelongsToPartner(permissions.BasePermission):
    """
        Permission that allows authenticated partners to retrieve or edit profiles that
        belongs to them.
    """
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or isinstance(obj, ProfileAttributeDocument) or isinstance(obj, Analysis):
            return True
        
        partner = Partner.get_authenticated_partner(request)
        try:
            Profile.objects.get(pk=obj.id, partner=partner)
            return True
        except Profile.DoesNotExist:
            raise PermissionDenied({
                    "code": status.HTTP_403_FORBIDDEN,
                    "message": "Permission Error",
                    "details":[
                        {"error": "The profile you are trying to retrieve or edit does not belong to you."}
                    ]
                })
            
        return True
    

class IsAdminToDeletePut(permissions.BasePermission):
    """
        Permission that ONLY allows an admin to DELETE or PUT.
    """
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE']:
            if not request.user.is_staff:
                raise PermissionDenied({
                        "code": status.HTTP_403_FORBIDDEN,
                        "message": "Permission Error",
                        "details":[
                            {"error": "You must be an admin to perform this action."}
                        ]
                    })
            
        return True
    

