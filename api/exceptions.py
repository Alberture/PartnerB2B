from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

from permissions import BelongsToPartnerToGetPatch

from datetime import datetime

def error_response_template(message, status, details):
    return {
            "error": {
                'message' : message,
                'code' : status,
                'details': details
            },
            "meta":{
                "timestamp": datetime.now()
            }
        }

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError' : _handle_validation_error,
        'NotAuthenticated' : _handle_authentication_error,
        'PermissionDenied': _handle_permission_error,
        'ObjectDoesNotExist': _handle_object_does_not_exist,
        'ValueError': _handle_value_error,
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
    if response : 
        response.data = error_response_template(
            'Authentication Error',
              response.status_code,
              [{'error': "The token either expired or is invalid."}]
            )

    return response

def _handle_validation_error(exc, context, response):
    if not response:
        return Response(exc.args[0])

    fields = response.data.keys()
    response.data = error_response_template(
        'Validation Error.',
        response.status_code,
        [
            {
                "field": next(iter(fields)),
                'error': response.data[next(iter(fields))]
            }
        ]
    )
    return response

def _handle_permission_error(exc, context, response):
    if not response:
        return Response(exc.args[0])
    
    response.data = error_response_template(
        'Permission Error.',
        response.status_code,
        [{'error': "You are not allowed to perform this action."}]
    )
    return response

def _handle_object_does_not_exist(exc, context, response):
    if not response:
        return Response(exc.args[0])
    return response

def _handle_value_error(exc, context, response):
    if not response:
        return Response(exc.args[0])
    return response


