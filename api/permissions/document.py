from rest_framework import permissions, status

from ..models import Profile, Partner

from rest_framework.exceptions import PermissionDenied

class DocumentBelongsToPartnerToRead(permissions.BasePermission):
    """
        Permission that allows authenticated partners to retrieve documents of
        THEIR Profiles ONLY.
    """
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if request.method in ['GET', 'PATCH', 'POST']:
            partner = Partner.get_authenticated_partner(request)
            try:
                Profile.objects.get(pk=obj.profile.id, partner=partner)
                return True
            except Profile.DoesNotExist:
                raise PermissionDenied({
                        "code": status.HTTP_403_FORBIDDEN,
                        "message": "Permission Error",
                        "details":[
                            {
                                "error": "The document you are trying to retrieve or edit does not belong to you.",
                                "action": request.method,
                                "path": request.path
                            }
                        ]
                    })
            
        return True
