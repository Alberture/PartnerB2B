from django.http import JsonResponse
from api.utils import error_response_template

def custom_404_view(request, exception=None):
    return JsonResponse(error_response_template({
        "code": 404,
        "message": "Page not found",
        "details": "This url doesn't exist."}, request),
        status=404)

def custom_500_view(request, exception=None):
    return JsonResponse(error_response_template({
        "code": 500,
        "message": "Internal Error",
        "details": "There is an internal problem. Please try again."}, request),
        status=500
    )