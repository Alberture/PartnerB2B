from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

from ..serializers import ProfileSerializer, ProfileAttributeSerializer
from ..models import Partner

class ProfileViewSet(ViewSet):
    
    def create(self, request, *args, **kwargs):
        
        validated_token = JWTAuthentication().get_validated_token(request.META['HTTP_AUTHORIZATION'][7:])
        user_like_partner = JWTAuthentication().get_user(validated_token)
        partner = Partner.objects.get(pk=user_like_partner.id)
        
        profile_serializer = ProfileSerializer(data=request.data)
        
        if profile_serializer.is_valid(raise_exception=True):
            profile_serializer.save(partner=partner)
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)