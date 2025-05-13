from django.http import JsonResponse
from api.utils import error_response_template

def custom_404_view(request, exception=None):
    return JsonResponse(error_response_template(
        "Page not found",
        404,
        "This url doesn't exist."),
        status=404
    )