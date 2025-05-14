from rest_framework.response import Response
from rest_framework import status

from datetime import datetime

def valid_response(data, request_id, code=status.HTTP_200_OK):
    """
        Method that returns a Response object that contains the data, request id and status code
        given in params.

        param: dict data, status code, str request_id
        return: Response
    """
    return Response(
        {
            "data":data,
            "meta":{
                "timestamp": datetime.now(),
                "request_id": request_id
            }
        },
        status=code
    )

def error_response_template(data, request):
    """
        Method that to avoid rewritting the JSON for error messages.

        param: str message, status status, array details, str request_id
        return: dict
    """
    return {
            "error": data,
            "meta":{
                "timestamp": datetime.now(),
                "request_id": request.id
            }
        }