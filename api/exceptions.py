from rest_framework.views import exception_handler
from rest_framework.response import Response

from .utils import error_response_template

from datetime import datetime

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError' : _handle_validation_error,
        'NotAuthenticated' : _handle_authentication_error,
        'PermissionDenied': _handle_raised_error,
        'NotFound': _handle_raised_error,
        'MethodNotAllowed': _handle_raised_error
    }

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    exception_class = exc.__class__.__name__
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)

    return response

def _handle_authentication_error(exc, context, response):
    response.data = error_response_template({
            "code": response.status_code,
            "message": 'Authentication Error',
            "details": [
                {
                    'error': "Your token is either expired, invalid or wasn't set in headers."
                }
            ],
    }, context.get('request'))
    return response

def _handle_validation_error(exc, context, response):
    if response.data.get('message'):
        return Response(error_response_template(exc.args[0], context.get('request')))

    fields = response.data.keys()
    return Response(error_response_template({
        "code": response.status_code, 
        "message": "Validation Error", 
        "details": [
            {
                "field": next(iter(fields)),
                'error': response.data[next(iter(fields))]
            }
        ]
    }, context.get('request')))

def _handle_raised_error(exc, context, response):
    return Response(error_response_template(exc.args[0], context.get('request')))

