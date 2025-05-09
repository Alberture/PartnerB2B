from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.response import Response

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
        'NotFound' : _handle_404_error,
        'NotAuthenticated' : _handle_authentication_error,
        'PermissionDenied': _handle_permission_error,
        'ObjectDoesNotExist': _handle_object_does_not_exist,
        'ValueError': _handle_value_error
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
            'Erreur d\'authentification.',
              response.status_code,
              [{'error': "L'access token fourni est soit expiré ou non valide"}]
            )

    return response

def _handle_404_error(exc, context, response):
    if response : 
        response.data = error_response_template(
            'Erreur, page non trouvée.',
            response.status_code,
            [{'error': "Nous n\'avons pas pu trouver la page que vous cherchiez. Veuillez vérifier l\'url."}]
        )

    return response

def _handle_validation_error(exc, context, response):
    if not response:
        return Response(exc.args[0])
    else:
        fields = response.data.keys()
        response.data = error_response_template(
            'Erreur de validation.',
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
    if response:
        response.data = error_response_template(
            'Erreur de permission.',
            response.status_code,
            [{'error': "Vous n'êtes pas autorisé à réalise cette action"}]
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


