from rest_framework import permissions, status

from ..utils import get_authenticated_partner, get_profile_or_error
from ..models import Profile

from datetime import datetime

class BelongsToPartnerToGetPatch(permissions.BasePermission):
    
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
                return False
            
        return True
    

