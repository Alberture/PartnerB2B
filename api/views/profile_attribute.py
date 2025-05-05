from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from ..serializers import ProfileSerializer, ProfileAttributeSerializer
from ..models import Partner, Profile, Attribute

class ProfileViewSet(ViewSet):
    """
        ViewSet for Profile management (CRUD)
    """
    def create(self, request, *args, **kwargs):
            
        validated_token = JWTAuthentication().get_validated_token(request.META['HTTP_AUTHORIZATION'][7:])
        user_like_partner = JWTAuthentication().get_user(validated_token)
        partner = Partner.objects.get(pk=user_like_partner.id)
        profile_serializer = ProfileSerializer(data=request.data)
          
        if profile_serializer.is_valid(raise_exception=True):
            profile = profile_serializer.save(partner=partner)

            if request.data.get('attributes'):
                for name, value in request.data.get('attributes').items():
                    profile_attribute_serializer = ProfileAttributeSerializer(data=value)
                    if profile_attribute_serializer.is_valid():
                        attribute = Attribute.objects.get(name=name)
                        profile_attribute_serializer.save(attribute=attribute, profile=profile)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
                    
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
