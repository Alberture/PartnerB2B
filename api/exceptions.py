from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

from .utils import error_response

from datetime import datetime

def custom_exception_handler(exc, context):

    handlers = {
        'ValidationError' : _handle_validation_error,
        'Http404' : _handle_404_error,
        'NotAuthenticated' : _handle_authentication_error,
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

def _handle_404_error(exc, context, response):
    if response : 
        response.data = {
            "error": {
                'message' : 'Nous n\'avons pas pu trouver la page que vous cherchiez. Veuillez vérifier l\'url.',
                'code' : response.status_code,
                'details': []
            },
            "meta":{
                "timestamp": datetime.now()
            } 
        }
    return response

def _handle_validation_error(exc, context, response):
    if not response:
        return Response(exc.args[0])
    return response





