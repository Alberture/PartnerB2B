from rest_framework.views import exception_handler
from rest_framework import permissions

from .utils import error_response

from datetime import datetime

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError' : _handle_validation_error,
        'Http404' : _handle_generic_error,
        'PermissionDenied' : _handle_permissions_error,
        'NotAuthenticated' : _handle_authentication_error,
        'MethodNotAllowed': _handle_not_allowed_error,
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
    dd(context)
    if response : 
        response.data = {
            "error": {
                'message' : 'Please login to proceed',
                'code' : response.status_code,
                'details': []
            },
            "meta":{
                "timestamp": datetime.now()
            }
            
        }

    return response

def _handle_generic_error(exc, context, response):
    if response : 
        response.data = {
            "error": {
                'message' : 'Please login to proceed',
                'code' : response.status_code,
                'details': []
            },
            "meta":{
                "timestamp": datetime.now()
            }
            
        }

    return response

def _handle_validation_error(exc, context, response):
    if response : 
        response.data = {
            "error": {
                'message' : 'Please login to proceed',
                'code' : response.status_code,
                'details': [
                    
                ]
            },
            "meta":{
                "timestamp": datetime.now()
            }
            
        }

    return response

def _handle_not_allowed_error(exc, context, response):
    return response

def _handle_permissions_error(exc, context, response):
    return response



