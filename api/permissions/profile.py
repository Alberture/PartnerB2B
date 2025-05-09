from rest_framework import permissions, status

from ..utils import get_authenticated_partner, get_profile_or_error
from ..models import Profile

from datetime import datetime

class BelongsToPartnerToGetPatch(permissions.BasePermission):
    
    message = "Error Permission"
    #details = []

    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if request.method in ['GET', 'PATCH', 'POST']:
            partner = get_authenticated_partner(request)
            try:
                Profile.objects.get(pk=obj.id, partner=partner)
                return True
            except Profile.DoesNotExist:
                raise PermissionError({
                    "error": {
                        "code": status.HTTP_403_FORBIDDEN,
                        "message": "Permission Error",
                        "details": [
                            {"error": "The profile you are trying to retrieve or edit does not belong to you."}
                        ]
                    },
                    "meta": {
                        "timestamp": datetime.now()
                    }
                })
            
        raise PermissionError({
                    "error": {
                        "code": status.HTTP_403_FORBIDDEN,
                        "message": "Permission Error",
                        "details": [
                            {"error": "You must be an admin to perform this action."}
                        ]
                    },
                    "meta": {
                        "timestamp": datetime.now()
                    }
                }
            )
    
