from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from ..serializers import ProfileSerializer, ProfileAttributeSerializer, ProfileItemSerializer
from ..models import Partner, Profile, Attribute, ProfileAttribute


class ProfileViewSet(ModelViewSet):
    """
    ViewSet for Profile management (CRUD)
    """
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def create(self, request, *args, **kwargs):
        partner = self.get_authenticated_partner(request)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            profile = serializer.save(partner=partner)
            attributes = request.data.get('attributes', {})

            for name, value in attributes.items():
                attribute = self.get_attribute_or_error(name)
                if not attribute:
                    return self.error_response(f"L'attribut {name} n'existe pas.")

                if not self.process_attribute_value(value, attribute, profile):
                    return self.invalid_format_response()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return self.invalid_format_response()

    def retrieve(self, request, pk, *args, **kwargs):
        profile = self.get_profile_or_error(pk)
        if not profile:
            return self.error_response("Ce profil n'existe pas. Veuillez vérifier l'identifiant de l'utilisateur.")

        serializer = ProfileItemSerializer(profile)
        return Response(serializer.data)

    def partial_update(self, request, pk, *args, **kwargs):
        profile = self.get_profile_or_error(pk)
        if not profile:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():
            profile = serializer.save()
            attributes = request.data.get('attributes', {})

            for name, value in attributes.items():
                attribute = self.get_attribute_or_error(name)
                if not attribute:
                    return self.error_response(f"L'attribut {name} n'existe pas.")

                profile_attribute_qs = ProfileAttribute.objects.filter(profile=profile, attribute=attribute)

                if isinstance(value, list):
                    profile_attribute_qs.delete()

                if not self.process_attribute_value(value, attribute, profile, profile_attribute_qs.first()):
                    return self.invalid_format_response()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='submit')
    def submit(self, request, pk=None):
        profile = self.get_profile_or_error(pk)
        if not profile:
            return self.error_response("Nous n'avons pas pu trouver ce profil. Veuillez vérifier l'identifiant de l'utilisateur.")

        profile.status = 'complete'
        profile.save()

        return Response({
            'status': 'Complet',
            'message': 'Ce profil a été marqué comme complet et prêt pour analyse.'
        })

    def get_authenticated_partner(self, request):
        token_str = request.META.get('HTTP_AUTHORIZATION', '')[7:]
        validated_token = JWTAuthentication().get_validated_token(token_str)
        user = JWTAuthentication().get_user(validated_token)
        return Partner.objects.get(pk=user.id)

    def get_profile_or_error(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except Profile.DoesNotExist:
            return None

    def get_attribute_or_error(self, name):
        try:
            return Attribute.objects.get(name=name)
        except Attribute.DoesNotExist:
            return None

    def process_attribute_value(self, value, attribute, profile, instance=None):
        if isinstance(value, list):
            for choice in value:
                if not self.save_value(choice, attribute, profile):
                    return False
        else:
            if not self.save_value(value, attribute, profile, instance):
                return False
        return True

    def save_value(self, value, attribute, profile, instance=None):
        serializer = ProfileAttributeSerializer(data={'value': value}, instance=instance)
        if serializer.is_valid():
            serializer.save(attribute=attribute, profile=profile)
            return True
        return False

    def error_response(self, message):
        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    def invalid_format_response(self):
        return self.error_response("Le format des données n'est pas respecté")
