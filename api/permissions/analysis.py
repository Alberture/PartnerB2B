from rest_framework import permissions, status

from ..models import Profile, Partner

from rest_framework.exceptions import PermissionDenied, Throttled

class AnalysisBelongsToPartnerToRead(permissions.BasePermission):
    """
        Permission that allows authenticated partners to retrieve analysis of
        THEIR Profiles ONLY.
    """
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or isinstance(obj, Profile):
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
                            {"error": "The analysis you are trying to retrieve or edit does not belong to you."}
                        ]
                    },
                )
            
        return True

class IsAdminOrHasEnoughTries(permissions.BasePermission):
    """
        Permission that allows to do analysis if the partner has enough
        permissions or is admin.
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        
        if request.method == 'POST':
            partner = Partner.get_authenticated_partner(request)
            if not partner.limitUsage > 0:
                raise PermissionDenied({
                        "code": status.HTTP_429_TOO_MANY_REQUESTS,
                        "message": "Permission Error",
                        "details":[
                            {
                                "field": "limitUsage",
                                "error": "You have reached the limit usage you had."
                            }
                        ]
                    })

        return True