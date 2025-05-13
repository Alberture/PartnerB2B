from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import ValidationError, NotFound

from django.core.exceptions import ObjectDoesNotExist

from ..models import Partner, Profile, Attribute, ProfileAttributeDocument, Analysis
from ..serializers import ProfileAttributeSerializer
from datetime import datetime

def get_authenticated_partner(request):
    """
        Method that returns the authenticated
        Partner sending the request.

        param: request
        return: Partner
    """
    token_str = request.META.get('HTTP_AUTHORIZATION', '')[7:]
    validated_token = JWTAuthentication().get_validated_token(token_str)
    user = JWTAuthentication().get_user(validated_token)
    return Partner.objects.get(pk=user.id)

def get_profile_or_error(pk):
    """
        Method that returns a Profile with the given id, raises an
        exception if the Profile was not found or pk is invalid.

        param: int pk, id of the Profile
        return: Profile
        exceptions: NotFound, ValueError
    """
    try:
        return Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        raise NotFound(error_response_template(
                "Profile Not Found", 
                status.HTTP_404_NOT_FOUND, [{
                "field": "pk",
                "error": "This profile id does not exist. Please try again."
                }]
            )
        )
    except ValueError:
        raise ValidationError(error_response_template(
            "Type Error", 
            status.HTTP_400_BAD_REQUEST,[{
                "field": "pk",
                "error": "The profile id must be an integer."
                }]
            )
        )

def get_attribute_or_error(name):
    """
        Method that returns an Attribute with the given id or
        raises an exception if the Attribute was not found
        or pk is invalid.

        param: int pk, id of the Attribute
        return: Attribute
        exceptions: NotFound, ValueError
    """
    try:
        return Attribute.objects.get(name=name)
    except Attribute.DoesNotExist:
        raise NotFound(error_response_template(
            "Attribute Not Found",
            status.HTTP_404_NOT_FOUND,[{
                "field": "name",
                "error": "This attribute name does not exist. Please try again"
                }]
            )
        )
    except ValueError:
        raise ValidationError(error_response_template(
            "Type Error",
            status.HTTP_400_BAD_REQUEST,[{
                    "field": "name",
                    "error": "The attribute name must be a string."
                    }]
                )
            )

def get_docuement_or_error(pk):
    """
        Method that returns a ProfileAttributeDocument with the given id or 
        raises an exception if the ProfileAttributeDocument was not found
        or pk is invalid.

        param: int pk, id of the ProfileAttributeDocument
        return: ProfileAttributeDocument
        exceptions: NotFound, ValueError
    """
    try:
        return ProfileAttributeDocument.objects.get(pk=pk)
    except ProfileAttributeDocument.DoesNotExist:
        raise NotFound(error_response_template(
            "ProfileAttributeDocument Not Found",
            status.HTTP_404_NOT_FOUND,[{
                    "field": "pk",
                    "error": "This document id does not exist. Please try again"
                    }]
                )    
            )

    except ValueError:
        raise ValidationError(error_response_template(
            "TypeError",
            status.HTTP_400_BAD_REQUEST,[{
                    "field": "pk",
                    "error": "The document id must be an integer"
                    }]
                )
            )
    
def get_analysis_or_error(pk):
    """
        Method that returns an Analysis with the given id or 
        raises an exception if the Analysis was not found
        or pk is invalid.

        param: int pk, id of the Analysis
        return: Analysis
        exceptions: NotFound, ValueError
    """
    try:
        return Analysis.objects.get(pk=pk)
    except Analysis.DoesNotExist:
        raise NotFound(error_response_template(
            "Analysis not found",
            status.HTTP_404_NOT_FOUND,[{
                    "field": "pk",
                    "error": "This analysis does not exist. Please try again."
                    }]
                )
            )
    
    except ValueError:
        raise ValidationError(error_response_template(
            "Type Error",
            status.HTTP_400_BAD_REQUEST,[{
                    "field": "pk",
                    "error": "The analysis id must be an integer."
                    }]
                )
            )
    
def get_partner_or_error(apiKey):
    """
        Method that returns a Partner with the given id or 
        raises an exception if the AnalPartnerysis was not found
        or pk is invalid.

        param: int pk, id of the Partner
        return: Partner
        exceptions: NotFound, ValueError
    """
    try:
        return Partner.objects.get(apiKey=apiKey)
    except Partner.DoesNotExist:
        raise NotFound(error_response_template(
            "Partner not found",
            status.HTTP_404_NOT_FOUND,[{
                    "field": "apiKey",
                    "error": "The API key was not found."
                    }]
                )
            )
    
    except ValueError:
        raise ValidationError(error_response_template(
            "Type Error",
            status.HTTP_400_BAD_REQUEST,[
                {
                "field": "pk",
                "error": "The partner id must be an integer."
                }
            ]
            )
        )

def save_value(value, attribute, profile, instance=None):
    """
        Method that creates a ProfileAttribute with the given Attribute,
        Profile and value or edits an instance of ProfileAttribute.

        param: any value, Attribute attribute, Profile profile, ProfileAttribute instance 
        return: ProfileAttribute
        exceptions: ValidationError, NotFound
    """
    serializer = ProfileAttributeSerializer(data={'value': value}, instance=instance)
    serializer.is_valid(raise_exception=True)
    return serializer.save(attribute=attribute, profile=profile)

def valid_response(data, request_id, code=status.HTTP_200_OK):
    """
        Method that returns a Response object that contains the data and status code
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

def error_response_template(message, status, details):
    """
        Method that to avoid rewritting the JSON for message 
        error.

        param: str message, status status, array details, str request_id
        return: dict
    """
    return {
            "error": {
                'code' : status,
                'message' : message,
                'details': details
            },
            "meta":{
                "timestamp": datetime.now(),
            }
        }