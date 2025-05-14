from rest_framework import permissions, status

from ..models import Profile, Partner

from rest_framework.exceptions import PermissionDenied, MethodNotAllowed

class AnalysisBelongsToPartner(permissions.BasePermission):
    """
        Permission that allows authenticated partners to retrieve and edit analysis of
        THEIR Profiles ONLY.
    """
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
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

class IsAdminOrHasEnoughTries(permissions.BasePermission):
    """
        Permission that allows to do analysis if the partner has enough
        permissions or is admin.
    """
    def has_permission(self, request, view):
        if request.user.is_staff :
            return True
        
        if request.method == 'POST' and "analyses" in request.path:
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