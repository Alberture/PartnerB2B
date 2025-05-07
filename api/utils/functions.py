from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Partner, Profile, Attribute, ProfileAttributeDocument
from ..serializers import ProfileAttributeSerializer

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
        Method that returns a Profile with the given id
        or None if the Profile was not found

        param: int pk, id of the Profile
        return: Profile
    """
    try:
        return Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return None

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
        return None

def get_docuement_or_error(pk):
    try:
        return ProfileAttributeDocument.objects.get(pk=pk)
    except Attribute.DoesNotExist:
        return None


def save_value(value, attribute, profile, instance=None):
    """
        Method that saves or not a value in a new 
        ProfileAttribute object or instance.
        Mainly created to make the code more 
        readable.

        param: 
            string value
            Attribute attribute
            Profile profile
            ProfileAttribute instance
        
        return: Boolean
    """
    serializer = ProfileAttributeSerializer(data={'value': value}, instance=instance)
    if serializer.is_valid():
        serializer.save(attribute=attribute, profile=profile)
        return True
    return False

def process_attribute_value(value, attribute, profile, instance=None):
    """
        Method is returns False if a value couldn't be saved in
        a ProfileAttribute object and True if everything was saved

        param: 
            string value
            Attribute attribute
            Profile profile
            ProfileAttribute instance
        
        return: Boolean
    """
    if isinstance(value, list):
        for choice in value:
            if not save_value(choice, attribute, profile):
                return False
    else:
        if not save_value(value, attribute, profile, instance):
            return False
    return True


def error_response(message):
    """
        Method that returns a Response with a custom message

        param: string message
        return Response
    """
    return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)