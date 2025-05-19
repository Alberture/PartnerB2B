from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

from .utils import error_response_template

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError' : _handle_validation_error,
        'NotAuthenticated' : _handle_authentication_error,
        'PermissionDenied': _handle_permission_denied_error,
        'NotFound': _handle_not_found_error,
        'MethodNotAllowed': _handle_method_not_allowed_error,
        'ParseError': _handle_parse_error,
        'InvalidToken': _handle_invalid_token,
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
    if exc.args[0]:
        return Response(error_response_template(exc.args[0], context.get('request')), status=status.HTTP_400_BAD_REQUEST)
    
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
    }, context.get('request')), status.HTTP_400_BAD_REQUEST)

def _handle_method_not_allowed_error(exc, context, response):
    if exc.args[0] in ['PUT', 'DELETE','PATCH', 'GET', 'POST']:
        return Response(error_response_template({
            "code": response.status_code,
            "message": "Not Allowed",
            "details":[
                {
                    "error": response.data['detail'],
                    "path": context.get('request').path
                }
            ]
        }, context.get('request')), status.HTTP_403_FORBIDDEN)

    return Response(error_response_template(exc.args[0], context.get('request')), status=status.HTTP_403_FORBIDDEN)

def _handle_permission_denied_error(exc, context, response):
   return Response(error_response_template(exc.args[0], context.get('request')), status=status.HTTP_403_FORBIDDEN)

def _handle_not_found_error(exc, context, response):
   return Response(error_response_template(exc.args[0], context.get('request')), status=status.HTTP_404_NOT_FOUND)

def _handle_parse_error(exc, context, response):
    return Response(error_response_template({
        "code": response.status_code,
        "message": "Parse Error",
        "details":[
            {
                "error": response.data.get('detail')
            }
        ]
    }, context.get('request')), status=status.HTTP_400_BAD_REQUEST)

def _handle_invalid_token(exc, context, response):
    return Response(error_response_template({
        "code": response.status_code,
        "message": response.data['messages'],
        "details": response.data['detail']
    }, context.get('request')), status=status.HTTP_401_UNAUTHORIZED)
