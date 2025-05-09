from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

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

def get_profile_or_error(pk, partner):
    """
        Method that returns a Profile with the given id and partner
        or None if the Profile was not found

        param: int pk, id of the Profile
        return: Profile
    """
    try:
        return Profile.objects.get(pk=pk, partner=partner)
    except Profile.DoesNotExist:
        raise ObjectDoesNotExist({
            "error":{
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Profil non trouvé",
                "details":[
                    {
                    "field": "pk",
                    "error": "Cet identifiant de profil n'existe pas. Veuillez vérifier l'identifiant."
                    }
                ]
            },
            "meta": {
                "timestamp": datetime.now()
            }
        })
    except ValueError:
        raise ValueError({
            "error":{
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Erreur de type",
                "details":[
                    {
                    "field": "pk",
                    "error": "L'identifiant du profile est un entier naturel."
                    }
                ]
            },
            "meta": {
                "timestamp": datetime.now()
            }
        })

def get_attribute_or_error(name):
    """
        Method that returns an Attribute with the given id
        or None if the Profile was not found

        param: int pk, id of the Attribute
        return: Attribute
    """
    try:
        return Attribute.objects.get(name=name)
    except Attribute.DoesNotExist:
        raise ObjectDoesNotExist({
            "error":{
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Attribut non trouvé",
                "details":[
                    {
                    "field": "name",
                    "error": "Cet attribut n'existe pas. Veuillez vérifier le nom de l'attribut."
                    }
                ]
            },
            "meta": {
                "timestamp": datetime.now()
            }
        })
    except ValueError:
        raise ValueError({
            "error":{
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Erreur de type",
                "details":[
                    {
                    "field": "name",
                    "error": "L'identifiant du profile est une chaine de caractère."
                    }
                ]
            },
            "meta": {
                "timestamp": datetime.now()
            }
        })

def get_docuement_or_error(pk):
    try:
        return ProfileAttributeDocument.objects.get(pk=pk)
    except Attribute.DoesNotExist:
        raise ObjectDoesNotExist({
            "error":{
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Valeur associé au profile non trouvé",
                "details":[
                    {
                    "field": "pk",
                    "error": "Cette valeur associé n'existe pas. Veuillez vérifier l'identifiant de cette dernière."
                    }
                ]
            },
            "meta": {
                "timestamp": datetime.now()
            }
        })
    except ValueError:
        raise ValueError({
            "error":{
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Erreur de type",
                "details":[
                    {
                    "field": "pk",
                    "error": "L'identifiant d'un document est un entier naturel."
                    }
                ]
            },
            "meta": {
                "timestamp": datetime.now()
            }
        })
    
def get_analysis_or_error(pk):
    try:
        return Analysis.objects.get(pk=pk)
    except Attribute.DoesNotExist:
        raise ObjectDoesNotExist({
            "error":{
                "code": status.HTTP_404_NOT_FOUND,
                "message": "Analyse non trouvé",
                "details":[
                    {
                    "field": "pk",
                    "error": "Cette Analyse n'existe pas. Veuillez vérifier l'identifiant."
                    }
                ]
            },
            "meta": {
                "timestamp": datetime.now()
            }
        })
    except ValueError:
        raise ValueError({
            "error":{
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Erreur de type",
                "details":[
                    {
                    "field": "pk",
                    "error": "L'identifiant de l'analyse est un entier naturel."
                    }
                ]
            },
            "meta": {
                "timestamp": datetime.now()
            }
        })

def save_value(value, attribute, profile, instance=None):
    serializer = ProfileAttributeSerializer(data={'value': value}, instance=instance)
    serializer.is_valid(raise_exception=True)
    serializer.save(attribute=attribute, profile=profile)
    
def error_response(message, details=[], code=status.HTTP_400_BAD_REQUEST):
    """
        Method that returns a Response with a custom message

        param: string message
        return Response
    """
    return Response(
        {
            "error":{
                "code": code,
                "message": message,
                "details": details,
            },
            "meta":{
                "timestamp": datetime.now()
            }
        }, 
        status=code
    )
        

def valid_response(data, code=status.HTTP_200_OK):
    return Response(
        {
            "data":data,
            "meta":{
                "timestamp": datetime.now()
            }
        },
        status=code
    )