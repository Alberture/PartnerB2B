from rest_framework import permissions, status

from ..utils import get_authenticated_partner
from ..models import Profile

from django.core.exceptions import PermissionDenied

from datetime import datetime


class AnalysisBelongsToPartnerToGetPatch(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        if request.method in ['GET', 'PATCH', 'POST']:
            partner = get_authenticated_partner(request)
            try:
                Profile.objects.get(pk=obj.profile.id, partner=partner)
                return True
            except Profile.DoesNotExist:
                raise PermissionDenied({
                    "error":{
                        "code": status.HTTP_403_FORBIDDEN,
                        "message": "Permission Error",
                        "details":[
                            {"error": "The analysis you are trying to retrieve or edit does not belong to you."}
                        ]
                    },
                    "meta":{
                        "timestamp": datetime.now()
                    }
                })
            
        return True


    