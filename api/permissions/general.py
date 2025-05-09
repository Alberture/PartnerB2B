from rest_framework import permissions

class IsAdminToDeletePut(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'DELETE']:
            return request.user.is_staff
            
        return True

class IsAdminToDeletePutPatch(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_staff
            
        return True
    

