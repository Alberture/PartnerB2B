from rest_framework import permissions, status

from ..models import Profile, Analysis, ProfileAttributeDocument, Partner

from rest_framework.exceptions import PermissionDenied

class ProfileBelongsToPartner(permissions.BasePermission):
    """
        Permission that allows authenticated partners to retrieve, delete or edit profiles that
        belongs to them.
    """
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        partner = Partner.get_authenticated_partner(request)
        try:
            Profile.objects.get(pk=obj.id, partner=partner)
        except Profile.DoesNotExist:
            raise PermissionDenied({
                    "code": status.HTTP_403_FORBIDDEN,
                    "message": "Permission Error",
                    "details":[
                        {
                            "error": "The profile you are trying to retrieve, delete or edit does not belong to you.",
                            "action": request.method,
                            "path": request.path
                        }
                    ]
                })
            
        return True