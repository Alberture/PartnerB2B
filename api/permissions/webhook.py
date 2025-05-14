from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied

from ..models.partner import Partner
from ..models.webhook import Webhook

class WebhookBelongsToParnter(permissions.BasePermission):
    """
        Permission that ONLY allows a partner to configure a webkooh.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        
        partner = Partner.get_authenticated_partner(request)
        try:
            Webhook.objects.get(pk=obj.id, partner=partner)
            return True
        except Webhook.DoesNotExist:
            raise PermissionDenied({
                "code": status.HTTP_403_FORBIDDEN,
                "message": "Permission Error",
                "details":[
                    {
                        "error": "The webhook you are trying to edit or delete does not belong to you.",
                        "action": request.method,
                        "path": request.path
                    }
                ] 
            })

        

