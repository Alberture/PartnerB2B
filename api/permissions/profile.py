from rest_framework import permissions

from ..utils import get_authenticated_partner, get_profile_or_error
from ..models import Profile

class BelongsToPartnerToGetPatch(permissions.BasePermission):
  
    def has_permission(self, request, view):
        return True  # ou ta logique globale
    
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
            
        return False
    
